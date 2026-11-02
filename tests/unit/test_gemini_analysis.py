"""Unit tests for the Gemini analysis script: token limits, quota handling and truncation."""

import io
import json
import sys
from pathlib import Path
from urllib import error

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github" / "scripts"))

import gemini_analysis
from gemini_analysis import (
    ApiError,
    estimate_tokens,
    extract_analysis,
    finish_reason,
    format_usage,
    generate_analysis,
    parse_api_error,
    parse_model_limits,
)

RETRY_429 = json.dumps(
    {
        "error": {
            "code": 429,
            "message": "Quota exceeded for metric",
            "status": "RESOURCE_EXHAUSTED",
            "details": [
                {
                    "@type": "type.googleapis.com/google.rpc.QuotaFailure",
                    "violations": [{"quotaId": "GenerateContentInputTokensPerModelPerMinute-FreeTier"}],
                },
                {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "27s"},
            ],
        }
    }
)
DAILY_429 = json.dumps(
    {
        "error": {
            "code": 429,
            "message": "daily quota",
            "details": [
                {
                    "@type": "type.googleapis.com/google.rpc.QuotaFailure",
                    "violations": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}],
                },
                {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "30s"},
            ],
        }
    }
)


def _ok(text: str = "analysis", reason: str = "STOP") -> dict:
    """Build a minimal successful Gemini response."""
    return {
        "candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": reason}],
        "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "thoughtsTokenCount": 7, "totalTokenCount": 22},
    }


class _FakeGemini:
    """Scripted replacement for `call_model` that records the request bodies per model."""

    def __init__(self, script: dict) -> None:
        """Map each model to the list of outcomes returned by successive calls."""
        self.script = {model: list(outcomes) for model, outcomes in script.items()}
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, base_url, api_key, model, body):
        """Return the next scripted `(response, error)` for `model`."""
        self.calls.append((model, json.loads(body)))
        outcome = self.script[model].pop(0)
        return outcome if isinstance(outcome, tuple) else (outcome, None)


@pytest.fixture
def sleeps():
    """Collect requested sleeps instead of waiting."""
    return []


def _run(fake, models, sleeps, monkeypatch, **kwargs):
    """Run `generate_analysis` against the scripted model calls."""
    monkeypatch.setattr(gemini_analysis, "call_model", fake)
    return generate_analysis("prompt", models, 16384, "http://x", "key", sleep=sleeps.append, **kwargs)


def test_extract_analysis_skips_thought_parts_and_reads_finish_reason_and_usage() -> None:
    """Thought parts are dropped; finishReason and usage are exposed for diagnostics."""
    response = {
        "candidates": [
            {"content": {"parts": [{"text": "thinking", "thought": True}, {"text": "answer"}]}, "finishReason": "MAX_TOKENS"}
        ],
        "usageMetadata": {"promptTokenCount": 5661, "candidatesTokenCount": 6222, "thoughtsTokenCount": 6548, "totalTokenCount": 18431},
    }

    assert extract_analysis(response) == "answer"
    assert finish_reason(response) == "MAX_TOKENS"
    assert finish_reason({}) == ""
    assert format_usage(response) == "prompt=5661 output=6222 thoughts=6548 total=18431"
    assert format_usage({}) == ""


def test_estimate_tokens_is_conservative_for_the_measured_ratio() -> None:
    """The NRT prompt (17706 chars) measured 5661 tokens; the estimate must not be lower."""
    assert estimate_tokens("x" * 17706) >= 5661


def test_parse_api_error_reads_retry_delay_and_quota_ids() -> None:
    """RetryInfo and QuotaFailure details are decoded; a per-day quota is recognised."""
    minute = parse_api_error(429, RETRY_429)
    assert minute.retry_delay == 27.0
    assert not minute.daily_quota_exhausted
    assert parse_api_error(429, DAILY_429).daily_quota_exhausted
    plain = parse_api_error(500, "<html>boom</html>")
    assert plain.retry_delay is None and "boom" in plain.message


def test_parse_model_limits_validates_the_workflow_output() -> None:
    """Empty means no limits; malformed values fail loudly."""
    assert parse_model_limits("") == {}
    assert parse_model_limits('{"m": {"input": 10, "output": 5}}') == {"m": {"input": 10, "output": 5}}
    with pytest.raises(RuntimeError):
        parse_model_limits("[1]")
    with pytest.raises(RuntimeError):
        parse_model_limits("not json")


def test_call_model_translates_http_and_transport_errors(monkeypatch) -> None:
    """HTTP errors keep their retry hints; transport failures become a code-0 ApiError."""

    def raise_http(http_request, timeout):
        """Raise the 429 Gemini answers when the per-minute quota is exhausted."""
        raise error.HTTPError(http_request.full_url, 429, "Too Many Requests", {}, io.BytesIO(RETRY_429.encode()))

    monkeypatch.setattr(gemini_analysis.request, "urlopen", raise_http)
    response, api_error = gemini_analysis.call_model("http://x/v1beta", "key", "gemini-x", b"{}")
    assert response is None
    assert (api_error.code, api_error.retry_delay) == (429, 27.0)

    def raise_timeout(http_request, timeout):
        """Raise the timeout seen when the endpoint does not answer."""
        raise TimeoutError("timed out")

    monkeypatch.setattr(gemini_analysis.request, "urlopen", raise_timeout)
    response, api_error = gemini_analysis.call_model("http://x/v1beta", "key", "gemini-x", b"{}")
    assert response is None
    assert (api_error.code, api_error.message) == (0, "timed out")


def test_per_minute_429_waits_the_suggested_delay_then_succeeds(monkeypatch, sleeps) -> None:
    """A per-minute quota is retried once on the same model after the API's retryDelay."""
    fake = _FakeGemini({"a": [(None, parse_api_error(429, RETRY_429)), _ok("done")], "b": []})

    model, _, analysis = _run(fake, ["a", "b"], sleeps, monkeypatch)

    assert (model, analysis) == ("a", "done")
    assert sleeps == [27.0]
    assert [call[0] for call in fake.calls] == ["a", "a"]


def test_daily_quota_429_moves_to_the_next_model_without_waiting(monkeypatch, sleeps) -> None:
    """A per-day quota cannot be fixed by waiting, so the next model is used immediately."""
    fake = _FakeGemini({"a": [(None, parse_api_error(429, DAILY_429))], "b": [_ok("from b")]})

    model, _, analysis = _run(fake, ["a", "b"], sleeps, monkeypatch)

    assert (model, analysis) == ("b", "from b")
    assert sleeps == []


def test_a_long_retry_delay_is_not_waited_for(monkeypatch, sleeps) -> None:
    """A retryDelay above the cap sends the run to the next model instead of stalling the job."""
    long_wait = ApiError(code=429, message="slow down", retry_delay=600.0)
    fake = _FakeGemini({"a": [(None, long_wait)], "b": [_ok("from b")]})

    model, _, _ = _run(fake, ["a", "b"], sleeps, monkeypatch)

    assert model == "b"
    assert sleeps == []


def test_rate_limit_is_retried_only_once_per_model(monkeypatch, sleeps) -> None:
    """Two consecutive 429s on a model exhaust it; the next model takes over."""
    again = (None, parse_api_error(429, RETRY_429))
    fake = _FakeGemini({"a": [again, again], "b": [_ok("from b")]})

    model, _, _ = _run(fake, ["a", "b"], sleeps, monkeypatch)

    assert model == "b"
    assert sleeps == [27.0]


def test_thinking_level_is_sent_and_dropped_when_the_model_rejects_it(monkeypatch, sleeps) -> None:
    """A 400 about thinking is retried once without thinkingConfig on the same model."""
    rejected = (None, ApiError(code=400, message="Thinking level 'low' is not supported for this model"))
    fake = _FakeGemini({"a": [rejected, _ok("ok")]})

    model, _, _ = _run(fake, ["a"], sleeps, monkeypatch, thinking_level="low")

    assert model == "a"
    first, second = (call[1]["generationConfig"] for call in fake.calls)
    assert first["thinkingConfig"] == {"thinkingLevel": "low"}
    assert "thinkingConfig" not in second


def test_no_thinking_config_without_a_level(monkeypatch, sleeps) -> None:
    """The request stays as before when no thinking level is requested."""
    fake = _FakeGemini({"a": [_ok()]})

    _run(fake, ["a"], sleeps, monkeypatch)

    assert fake.calls[0][1]["generationConfig"] == {"maxOutputTokens": 16384}


def test_model_limits_clamp_output_and_skip_models_that_cannot_fit(monkeypatch, sleeps) -> None:
    """Output is clamped to the model limit; a model with a too small input limit is never called."""
    fake = _FakeGemini({"tiny": [], "small-out": [_ok("ok")]})
    limits = {"tiny": {"input": 1, "output": 8192}, "small-out": {"input": 1_000_000, "output": 8192}}

    model, _, _ = _run(fake, ["tiny", "small-out"], sleeps, monkeypatch, model_limits=limits)

    assert model == "small-out"
    assert [call[0] for call in fake.calls] == ["small-out"]
    assert fake.calls[0][1]["generationConfig"]["maxOutputTokens"] == 8192


def test_empty_text_falls_through_to_the_next_model(monkeypatch, sleeps) -> None:
    """A response with only thinking text (cut by MAX_TOKENS) is not accepted as an analysis."""
    thought_only = {"candidates": [{"content": {"parts": [{"text": "hm", "thought": True}]}, "finishReason": "MAX_TOKENS"}]}
    fake = _FakeGemini({"a": [thought_only], "b": [_ok("real")]})

    model, _, analysis = _run(fake, ["a", "b"], sleeps, monkeypatch)

    assert (model, analysis) == ("b", "real")


def test_all_models_failing_raises(monkeypatch, sleeps) -> None:
    """When every model fails the run reports it instead of writing an empty analysis."""
    fake = _FakeGemini({"a": [(None, ApiError(code=500, message="x"))], "b": [(None, ApiError(code=0, message="timeout"))]})

    with pytest.raises(RuntimeError, match="All available Gemini fallback models failed"):
        _run(fake, ["a", "b"], sleeps, monkeypatch)


def test_main_flags_a_truncated_response_and_writes_usage(monkeypatch, tmp_path, capsys) -> None:
    """MAX_TOKENS output is published with a visible notice, a warning and the usage in the job summary."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("analyse this", encoding="utf-8")
    output_dir = tmp_path / "out"
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    monkeypatch.setenv("AVAILABLE_MODELS", '["a"]')
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    monkeypatch.setattr(gemini_analysis, "call_model", _FakeGemini({"a": [_ok("half an analy", reason="MAX_TOKENS")]}))
    monkeypatch.setattr(
        sys, "argv",
        ["gemini_analysis.py", "--prompt-file", str(prompt_file), "--output-dir", str(output_dir),
         "--max-output-tokens", "100", "--thinking-level", "low"],
    )

    assert gemini_analysis.main() == 0

    written = (output_dir / "analysis.md").read_text(encoding="utf-8")
    assert written.startswith("half an analy")
    assert "Analysis truncated" in written
    assert "::warning title=AI analysis truncated::" in capsys.readouterr().out
    summary_text = summary.read_text(encoding="utf-8")
    assert "thoughts=7" in summary_text
    assert "output truncated at the token limit" in summary_text


def test_main_complete_response_has_no_truncation_notice(monkeypatch, tmp_path) -> None:
    """A STOP response is written untouched."""
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("analyse this", encoding="utf-8")
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    monkeypatch.setenv("AVAILABLE_MODELS", '["a"]')
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr(gemini_analysis, "call_model", _FakeGemini({"a": [_ok("full analysis")]}))
    monkeypatch.setattr(
        sys, "argv",
        ["gemini_analysis.py", "--prompt-file", str(prompt_file), "--output-dir", str(tmp_path / "out"),
         "--max-output-tokens", "100"],
    )

    assert gemini_analysis.main() == 0

    assert (tmp_path / "out" / "analysis.md").read_text(encoding="utf-8") == "full analysis\n"
