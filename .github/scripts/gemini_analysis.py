"""Generate a report analysis through Gemini with ordered model fallback."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-output-tokens", required=True, type=int)
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


def call_model(
    base_url: str,
    api_key: str,
    model: str,
    body: bytes,
) -> dict[str, Any] | None:
    """Call one Gemini model and return its decoded response when successful."""
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
            return json.loads(http_response.read().decode("utf-8"))
    except error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        print(f"Model '{model}' returned HTTP {exc.code}: {message}", file=sys.stderr)
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Model '{model}' failed: {exc}", file=sys.stderr)
    return None


def generate_analysis(
    prompt: str,
    models: list[str],
    max_output_tokens: int,
    base_url: str,
    api_key: str,
) -> tuple[str, dict[str, Any], str]:
    """Try models in order and return the first non-empty analysis response."""
    body = json.dumps(
        {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_output_tokens},
        }
    ).encode("utf-8")

    for model in models:
        print(f"Calling {model} ...")
        response = call_model(base_url, api_key, model, body)
        if response is None:
            continue
        analysis = extract_analysis(response)
        if analysis:
            return model, response, analysis
        print(f"Model '{model}' returned no analysis text", file=sys.stderr)

    raise RuntimeError("All available Gemini fallback models failed")


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

    prompt = args.prompt_file.read_text(encoding="utf-8")
    selected_model, response, analysis = generate_analysis(
        prompt,
        models,
        args.max_output_tokens,
        base_url,
        api_key,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "response.json").write_text(
        json.dumps(response, indent=2), encoding="utf-8"
    )
    (args.output_dir / "analysis.md").write_text(f"{analysis}\n", encoding="utf-8")
    print(f"Selected model: {selected_model}")
    print(analysis)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())