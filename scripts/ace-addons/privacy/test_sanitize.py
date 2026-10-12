"""Unit tests for project-owned ACE privacy transformation."""

import copy
import unittest
from types import SimpleNamespace

from sanitize import ItalianVatRecognizer, sanitize_text, sanitize_trace


class StubAnalyzer:
    """Return fixed spans for each configured language."""

    def analyze(self, **kwargs):
        """Simulate Presidio's entity results without external models."""
        text = kwargs["text"]
        if "Mario Rossi" not in text:
            return []
        start = text.index("Mario Rossi")
        return [SimpleNamespace(
            start=start, end=start + len("Mario Rossi"),
            entity_type="PERSON", score=0.9,
        )]


class PrivacyTests(unittest.TestCase):
    """Test redaction, policy and schema-preserving field selection."""

    def setUp(self):
        """Create a minimal trace-shaped sample and fake analyzer."""
        self.policy = {
            "languages": {"en": "en_core_web_sm", "it": "it_core_news_sm"},
            "entities": ["PERSON"],
            "score_threshold": 0.7,
            "entity_thresholds": {},
            "fields": ["request_summary", "notes", "actions[].description",
                       "outcome.detail", "friction[].description", "corrects.reason"],
        }
        self.trace = {
            "task_id": "mario-rossi", "agent": "qa-analyst",
            "started_at": "2026-01-01T00:00:00Z",
            "playbook_bullets_seen": [], "playbook_bullets_cited": [],
            "request_summary": "Mario Rossi",
            "actions": [{"description": "Mario Rossi", "tool": "Mario Rossi"}],
            "outcome": {"status": "success", "detail": "Mario Rossi"},
            "friction": [{"description": "Mario Rossi", "recovered": True}],
            "notes": "Mario Rossi",
            "corrects": {
                "task_id": "mario-rossi", "agent": "qa-analyst",
                "reason": "Mario Rossi", "counter_adjustments": [],
            },
        }
        self.analyzer = StubAnalyzer()

    def test_sanitize_only_prose_and_merge_languages(self):
        """Preserve trace evidence while masking each selected prose field once."""
        original = copy.deepcopy(self.trace)
        sanitized = sanitize_trace(self.trace, self.analyzer, self.policy, [])
        self.assertEqual(sanitized["request_summary"], "<PERSON>")
        self.assertEqual(sanitized["actions"][0]["description"], "<PERSON>")
        self.assertEqual(sanitized["outcome"]["detail"], "<PERSON>")
        self.assertEqual(sanitized["friction"][0]["description"], "<PERSON>")
        self.assertEqual(sanitized["corrects"]["reason"], "<PERSON>")
        self.assertEqual(sanitized["notes"], "<PERSON>")
        self.assertEqual(sanitized["actions"][0]["tool"], original["actions"][0]["tool"])
        self.assertEqual(sanitized["task_id"], original["task_id"])
        self.assertEqual(sanitized["corrects"]["task_id"], original["corrects"]["task_id"])

    def test_deny_list_excludes_combined_technical_terms(self):
        """Do not mask known technical labels even when NER combines them."""
        class CombinedAnalyzer:
            """Simulate an NLP match covering two technical terms."""

            def analyze(self, **kwargs):
                """Report a high-confidence PERSON match over the whole text."""
                text = kwargs["text"]
                return [SimpleNamespace(start=0, end=len(text),
                                        entity_type="PERSON", score=0.9)]

        self.assertEqual(
            sanitize_text("Behave Gherkin", CombinedAnalyzer(), self.policy,
                          ["Behave", "Gherkin"]),
            "Behave Gherkin",
        )

    def test_italian_vat_checksum(self):
        """Reject invalid VAT check digits before returning a match."""
        recognizer = ItalianVatRecognizer()
        self.assertTrue(recognizer.validate_result("12345678903"))
        self.assertFalse(recognizer.validate_result("12345678904"))

    def test_existing_placeholder_not_replaced(self):
        """A retry must not nest replacements around earlier output."""
        class PlaceholderAnalyzer:
            """Simulate NER treating the replacement token as a person."""

            def analyze(self, **kwargs):
                """Return a match covering the placeholder."""
                return [SimpleNamespace(start=0, end=8, entity_type="PERSON", score=0.9)]

        self.assertEqual(
            sanitize_text("<PERSON>", PlaceholderAnalyzer(), self.policy, []),
            "<PERSON>",
        )


if __name__ == "__main__":
    unittest.main()
