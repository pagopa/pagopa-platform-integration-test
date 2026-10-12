"""Sanitize ACE trace prose using a project-owned Presidio policy."""

import json
import re
import sys
from pathlib import Path

import tldextract
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider


ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / "config" / "ace-addons" / "privacy"
ALLOWED_FIELDS = {
    "request_summary",
    "notes",
    "actions[].description",
    "outcome.detail",
    "friction[].description",
    "corrects.reason",
}


class ItalianVatRecognizer(PatternRecognizer):
    """Detect Italian VAT IDs only when their check digit is valid."""

    def __init__(self):
        """Register an Italian VAT pattern with Presidio."""
        super().__init__(
            supported_entity="IT_PIVA",
            supported_language="it",
            patterns=[Pattern("Italian VAT", r"\b(?:IT)?[0-9]{11}\b", 0.8)],
        )

    def validate_result(self, pattern_text):
        """Validate the 11-digit Italian VAT checksum."""
        digits = pattern_text.removeprefix("IT")
        if len(digits) != 11 or not digits.isdigit():
            return False
        total = 0
        for index, digit in enumerate(digits[:10]):
            value = int(digit)
            if index % 2:
                value *= 2
                if value > 9:
                    value -= 9
            total += value
        return (10 - total % 10) % 10 == int(digits[-1])


def load_policy():
    """Load and validate the supported declarative configuration."""
    policy = json.loads((CONFIG / "policy.json").read_text(encoding="utf-8"))
    deny_list = json.loads((CONFIG / "deny-list.json").read_text(encoding="utf-8"))
    languages = policy.get("languages")
    language_map = {"en": "en_core_web_sm", "it": "it_core_news_sm"}
    if isinstance(languages, dict):
        lang_values = list(languages.keys())
    elif isinstance(languages, list):
        lang_values = list(languages)
    else:
        lang_values = []
    if (
        set(policy) - {"mode", "allow_person_ner"} != {"languages", "entities", "score_threshold",
                        "entity_thresholds", "fields"}
        or not isinstance(languages, (dict, list))
        or not lang_values
        or any(not isinstance(lang, str) or lang not in language_map for lang in lang_values)
        or not isinstance(policy["entities"], list)
        or not policy["entities"]
        or any(not isinstance(entity, str) for entity in policy["entities"])
        or not isinstance(policy["score_threshold"], (int, float))
        or isinstance(policy["score_threshold"], bool)
        or not 0 <= policy["score_threshold"] <= 1
        or not isinstance(policy["entity_thresholds"], dict)
        or not set(policy["entity_thresholds"]) <= set(policy["entities"])
        or any(not isinstance(value, (float, int)) or isinstance(value, bool)
               or not 0 <= value <= 1
               for value in policy["entity_thresholds"].values())
        or not isinstance(policy["fields"], list)
        or len(policy["fields"]) != len(set(policy["fields"]))
        or not set(policy["fields"]) <= ALLOWED_FIELDS
        or not policy["fields"]
        or not isinstance(deny_list, list)
        or any(not isinstance(word, str) or not word for word in deny_list)
    ):
        raise ValueError("Invalid ACE privacy policy or deny-list")
    if isinstance(languages, list):
        policy["languages"] = {lang: language_map[lang] for lang in languages}
    return policy, deny_list


def build_analyzer(policy):
    """Initialize local NLP models and built-in recognizers for configured languages."""
    # Presidio's email validation calls tldextract; its bundled suffix snapshot
    # works offline and avoids implicit publicsuffix.org requests.
    tldextract.extract = tldextract.TLDExtract(suffix_list_urls=())
    language_map = policy["languages"] if isinstance(policy["languages"], dict) else {
        lang: {"en": "en_core_web_sm", "it": "it_core_news_sm"}[lang]
        for lang in policy["languages"]
    }
    languages = list(language_map.keys())
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": lang, "model_name": model}
                   for lang, model in language_map.items()],
    })
    registry = RecognizerRegistry(supported_languages=languages)
    registry.load_predefined_recognizers(languages=languages)
    if "it" in languages:
        registry.add_recognizer(ItalianVatRecognizer())
    available = {
        entity
        for language in languages
        for recognizer in registry.get_recognizers(language=language, all_fields=True)
        for entity in recognizer.supported_entities
    }
    missing = set(policy["entities"]) - available
    if missing:
        raise ValueError(f"No recognizer for configured entities: {sorted(missing)}")
    return AnalyzerEngine(
        nlp_engine=provider.create_engine(),
        registry=registry,
        supported_languages=languages,
    )


def sanitize_text(text, analyzer, policy, deny_list):
    """Replace detected spans without changing text outside those spans."""
    findings = []
    excluded = {item.casefold() for item in deny_list}
    placeholders = list(re.finditer(r"<[A-Z][A-Z_]+>", text))
    thresholds = policy["entity_thresholds"]
    for language in policy["languages"]:
        findings.extend(analyzer.analyze(
            text=text,
            language=language,
            entities=policy["entities"],
            score_threshold=min([policy["score_threshold"], *thresholds.values()]),
            allow_list=deny_list,
        ))
    findings.sort(key=lambda hit: (hit.entity_type == "PERSON", -hit.score,
                                   hit.start, hit.end))
    selected = []
    for hit in findings:
        if hit.score < thresholds.get(hit.entity_type, policy["score_threshold"]):
            continue
        if hit.start < 0 or hit.end > len(text) or hit.start >= hit.end:
            raise ValueError("Presidio returned invalid offsets")
        if any(hit.start < marker.end() and marker.start() < hit.end
               for marker in placeholders):
            continue
        if all(word.casefold() in excluded
               for word in text[hit.start:hit.end].split()):
            continue
        if any(hit.start < previous.end and previous.start < hit.end
               for previous in selected):
            continue
        selected.append(hit)
    for hit in sorted(selected, key=lambda item: item.start, reverse=True):
        text = text[:hit.start] + f"<{hit.entity_type}>" + text[hit.end:]
    return text


def sanitize_trace(trace, analyzer, policy, deny_list):
    """Transform only configured prose paths, preserving all ACE metadata."""
    for field in policy["fields"]:
        if "[]" in field:
            collection, key = field.split("[].")
            for item in trace.get(collection, []):
                item[key] = sanitize_text(item[key], analyzer, policy, deny_list)
        elif "." in field:
            parent, key = field.split(".")
            if parent in trace and key in trace[parent]:
                trace[parent][key] = sanitize_text(
                    trace[parent][key], analyzer, policy, deny_list
                )
        elif field in trace:
            trace[field] = sanitize_text(trace[field], analyzer, policy, deny_list)
    return trace


def main():
    """Read a trace from stdin and emit only sanitized JSON on stdout."""
    policy, deny_list = load_policy()
    trace = json.load(sys.stdin)
    analyzer = build_analyzer(policy)
    json.dump(sanitize_trace(trace, analyzer, policy, deny_list), sys.stdout,
              ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, ImportError) as error:
        print(f"ACE privacy sanitization failed: {error}", file=sys.stderr)
        sys.exit(1)
