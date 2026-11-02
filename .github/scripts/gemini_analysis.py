"""Generate a report analysis through Gemini with ordered model fallback.

Besides the model fallback the script protects the run against token limits:

* thinking tokens count toward `maxOutputTokens`, so a thinking level can be requested
  (`--thinking-level`) and is dropped for models that reject it;
* the per-model `inputTokenLimit` / `outputTokenLimit` from the model catalog (`MODEL_LIMITS`)
  clamp the output cap and skip models that cannot take the prompt;
* a 429 is retried once after the `retryDelay` suggested by the API, unless the daily quota is
  exhausted, in which case the next model is tried straight away;
* a response cut by `MAX_TOKENS` is flagged instead of being published as a complete analysis;
* the real token usage is logged and added to the job summary.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib import error, parse, request

# Conservative estimate: the NRT prompts measured ~3.1 characters per token.
CHARS_PER_TOKEN = 3.0
MAX_RETRY_WAIT_SECONDS = 60.0
DEFAULT_RATE_LIMIT_WAIT_SECONDS = 20.0
DEFAULT_OVERLOAD_WAIT_SECONDS = 5.0
TRUNCATION_NOTICE = (
    "> ⚠️ **Analysis truncated**: the model reached the output token limit before finishing. "
    "Some failures at the end may be missing; re-run with a higher `max_tokens` or fewer failures."
)


@dataclass
class ApiError:
    """A failed Gemini call: HTTP status (0 for transport errors), message and retry hints."""

    code: int
    message: str
    retry_delay: float | None = None
    quota_ids: list[str] = field(default_factory=list)

    @property
    def daily_quota_exhausted(self) -> bool:
        """Return True when the 429 refers to a per-day quota, which a short wait cannot fix."""
        return any("perday" in quota_id.lower() for quota_id in self.quota_ids)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-output-tokens", required=True, type=int)
    parser.add_argument(
        "--thinking-level",
        default="",
        help="Gemini thinkingLevel (e.g. low); empty keeps the model default",
    )
    return parser


def extract_analysis(response: dict[str, Any]) -> str:
    """Join non-thinking text parts from a Gemini response."""
    candidates = response.get("candidates") or []
    if not candidates:
        return ""
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    return "".join(
        str(part.get("text", ""))
        for part in parts
        if part.get("thought") is not True
    ).strip()


def finish_reason(response: dict[str, Any]) -> str:
    """Return the finishReason of the first candidate, or an empty string when absent."""
    candidates = response.get("candidates") or []
    if not candidates:
        return ""
    return str(candidates[0].get("finishReason") or "")


def format_usage(response: dict[str, Any]) -> str:
    """Return a one-line token usage summary from `usageMetadata`, empty when it is missing."""
    usage = response.get("usageMetadata") or {}
    if not usage:
        return ""
    return (
        f"prompt={usage.get('promptTokenCount', '?')} "
        f"output={usage.get('candidatesTokenCount', '?')} "
        f"thoughts={usage.get('thoughtsTokenCount', 0)} "
        f"total={usage.get('totalTokenCount', '?')}"
    )


def estimate_tokens(text: str) -> int:
    """Estimate the token count of `text` without calling the API (deliberately on the high side)."""
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def parse_model_limits(raw: str) -> dict[str, dict[str, int]]:
    """Parse the `MODEL_LIMITS` JSON object `{model: {"input": n, "output": n}}`; empty input gives `{}`.

    Raises RuntimeError when the value is not such an object, so a broken workflow wiring is visible.
    """
    if not raw.strip():
        return {}
    try:
        limits = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"MODEL_LIMITS is not valid JSON: {exc}") from exc
    if not isinstance(limits, dict) or not all(isinstance(value, dict) for value in limits.values()):
        raise RuntimeError("MODEL_LIMITS must be a JSON object of per-model limit objects")
    return limits


def parse_api_error(code: int, raw: str) -> ApiError:
    """Build an ApiError from an HTTP error body, reading Google's `RetryInfo` and `QuotaFailure` details."""
    message = raw.strip()[:500]
    retry_delay: float | None = None
    quota_ids: list[str] = []
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = None
    error_body = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error_body, dict):
        message = str(error_body.get("message") or message)[:500]
        for detail in error_body.get("details") or []:
            if not isinstance(detail, dict):
                continue
            detail_type = str(detail.get("@type", ""))
            if detail_type.endswith("RetryInfo"):
                match = re.fullmatch(r"(\d+(?:\.\d+)?)s", str(detail.get("retryDelay", "")))
                retry_delay = float(match.group(1)) if match else retry_delay
            elif detail_type.endswith("QuotaFailure"):
                quota_ids.extend(
                    str(violation.get("quotaId", ""))
                    for violation in detail.get("violations") or []
                    if isinstance(violation, dict)
                )
    return ApiError(code=code, message=message, retry_delay=retry_delay, quota_ids=quota_ids)


def build_body(prompt: str, max_output_tokens: int, thinking_level: str) -> bytes:
    """Encode the generateContent request, with a thinking level only when one is requested."""
    generation_config: dict[str, Any] = {"maxOutputTokens": max_output_tokens}
    if thinking_level:
        generation_config["thinkingConfig"] = {"thinkingLevel": thinking_level}
    return json.dumps(
        {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }
    ).encode("utf-8")


def call_model(
    base_url: str,
    api_key: str,
    model: str,
    body: bytes,
) -> tuple[dict[str, Any] | None, ApiError | None]:
    """Call one Gemini model; return `(response, None)` on success or `(None, ApiError)` on failure."""
    model_path = parse.quote(model, safe="")
    endpoint = f"{base_url.rstrip('/')}/models/{model_path}:generateContent"
    http_request = request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
    )
    try:
        with request.urlopen(http_request, timeout=120) as http_response:
            return json.loads(http_response.read().decode("utf-8")), None
    except error.HTTPError as exc:
        api_error = parse_api_error(exc.code, exc.read().decode("utf-8", errors="replace"))
        print(f"Model '{model}' returned HTTP {exc.code}: {api_error.message}", file=sys.stderr)
        return None, api_error
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Model '{model}' failed: {exc}", file=sys.stderr)
        return None, ApiError(code=0, message=str(exc))


def call_with_recovery(
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    max_output_tokens: int,
    thinking_level: str,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any] | None:
    """Call one model, recovering from the failures that a different request or a short wait can fix.

    A 400 that complains about thinking is retried once without `thinkingConfig`; a 429 (not a daily
    quota) or 503 is retried once after the delay suggested by the API, if it is short enough.
    Anything else gives up on this model so the caller can fall back to the next one.
    """
    waited = False
    for _ in range(3):
        body = build_body(prompt, max_output_tokens, thinking_level)
        response, api_error = call_model(base_url, api_key, model, body)
        if api_error is None:
            return response

        if api_error.code == 400 and thinking_level and "thinking" in api_error.message.lower():
            print(f"Model '{model}' rejected thinkingLevel '{thinking_level}'; retrying without it", file=sys.stderr)
            thinking_level = ""
            continue

        retryable = api_error.code == 503 or (api_error.code == 429 and not api_error.daily_quota_exhausted)
        if retryable and not waited:
            default_wait = DEFAULT_OVERLOAD_WAIT_SECONDS if api_error.code == 503 else DEFAULT_RATE_LIMIT_WAIT_SECONDS
            wait = api_error.retry_delay if api_error.retry_delay is not None else default_wait
            if wait <= MAX_RETRY_WAIT_SECONDS:
                print(f"Model '{model}' is rate limited; retrying in {wait:.0f}s", file=sys.stderr)
                sleep(wait)
                waited = True
                continue
        if api_error.code == 429 and api_error.daily_quota_exhausted:
            print(f"Model '{model}' exhausted its daily quota; trying the next model", file=sys.stderr)
        return None
    return None


def generate_analysis(
    prompt: str,
    models: list[str],
    max_output_tokens: int,
    base_url: str,
    api_key: str,
    thinking_level: str = "",
    model_limits: dict[str, dict[str, int]] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[str, dict[str, Any], str]:
    """Try models in order and return the first non-empty analysis response.

    `model_limits` (catalog `inputTokenLimit`/`outputTokenLimit`) clamps the output cap per model and
    skips a model whose input limit the estimated prompt size would exceed.
    """
    limits_by_model = model_limits or {}
    estimated_input = estimate_tokens(prompt)

    for model in models:
        limits = limits_by_model.get(model) or {}
        input_limit = int(limits.get("input") or 0)
        output_limit = int(limits.get("output") or 0)
        if input_limit and estimated_input > input_limit:
            print(
                f"Skipping '{model}': the prompt (~{estimated_input} tokens) exceeds its input limit ({input_limit})",
                file=sys.stderr,
            )
            continue
        output_cap = min(max_output_tokens, output_limit) if output_limit else max_output_tokens
        if output_cap < max_output_tokens:
            print(f"Clamping maxOutputTokens for '{model}' to its limit ({output_cap})")

        print(f"Calling {model} ...")
        response = call_with_recovery(
            base_url, api_key, model, prompt, output_cap, thinking_level, sleep=sleep
        )
        if response is None:
            continue
        analysis = extract_analysis(response)
        if analysis:
            return model, response, analysis
        print(
            f"Model '{model}' returned no analysis text (finishReason={finish_reason(response) or 'n/a'})",
            file=sys.stderr,
        )

    raise RuntimeError("All available Gemini fallback models failed")


def write_step_summary(model: str, estimated_input: int, usage: str, truncated: bool) -> None:
    """Append the token usage of the run to the GitHub job summary when one is available."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    lines = [
        "## Gemini token usage",
        "",
        f"- model: `{model}`",
        f"- estimated input: ~{estimated_input} tokens",
        f"- reported usage: {usage or 'n/a'}",
    ]
    if truncated:
        lines.append("- **output truncated at the token limit**")
    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write("\n".join(lines) + "\n")


def main() -> int:
    """Read workflow inputs, generate the analysis, and write artifact files."""
    args = build_parser().parse_args()
    base_url = os.environ.get(
        "BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
    )
    api_key = os.environ.get("GEMINI_API_KEY", "")
    models_json = os.environ.get("AVAILABLE_MODELS", "[]")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required")
    models = json.loads(models_json)
    if not isinstance(models, list) or not all(isinstance(model, str) for model in models):
        raise RuntimeError("AVAILABLE_MODELS must be a JSON array of model names")
    if not models:
        raise RuntimeError("AVAILABLE_MODELS contains no models")
    model_limits = parse_model_limits(os.environ.get("MODEL_LIMITS", ""))

    prompt = args.prompt_file.read_text(encoding="utf-8")
    selected_model, response, analysis = generate_analysis(
        prompt,
        models,
        args.max_output_tokens,
        base_url,
        api_key,
        thinking_level=args.thinking_level,
        model_limits=model_limits,
    )

    truncated = finish_reason(response) == "MAX_TOKENS"
    usage = format_usage(response)
    if truncated:
        print(
            "::warning title=AI analysis truncated::the model hit maxOutputTokens "
            f"({args.max_output_tokens}, thinking tokens included); {usage}"
        )
        analysis = f"{analysis}\n\n{TRUNCATION_NOTICE}"

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "response.json").write_text(
        json.dumps(response, indent=2), encoding="utf-8"
    )
    (args.output_dir / "analysis.md").write_text(f"{analysis}\n", encoding="utf-8")
    print(f"Selected model: {selected_model}")
    print(f"Token usage: {usage or 'n/a'} (estimated input ~{estimate_tokens(prompt)})")
    write_step_summary(selected_model, estimate_tokens(prompt), usage, truncated)
    print(analysis)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
