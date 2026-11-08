"""Thin LLM wrapper: anthropic | openai | mock (offline, for testing the loop)."""
import os
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"

# Deliberate factual errors used by the mock generator (and requested from real models).
ERROR_SWAPS = [
    ("There is no need to train the AI again.",
     "RAG retrains the model every night with your documents."),
    ("So RAG gives fewer wrong answers, but it does not remove them all.",
     "So RAG removes all wrong answers, and the AI never makes mistakes."),
]


class LLM:
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "mock")
        self.model = model
        if self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic()
            self.model = model or "claude-sonnet-4-5"
        elif self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI()
            self.model = model or "gpt-4o"

    @property
    def is_mock(self):
        return self.provider == "mock"

    def complete(self, system: str, user: str) -> str:
        if self.provider == "anthropic":
            r = self.client.messages.create(
                model=self.model, max_tokens=3000, system=system,
                messages=[{"role": "user", "content": user}])
            return r.content[0].text
        if self.provider == "openai":
            r = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}])
            return r.choices[0].message.content
        return self._mock(user)

    def _mock(self, user: str) -> str:
        text = (FIXTURES / "good_lesson.md").read_text()
        if "DELIBERATE_ERROR" in user:
            for good, bad in ERROR_SWAPS:
                text = text.replace(good, bad)
        return text
