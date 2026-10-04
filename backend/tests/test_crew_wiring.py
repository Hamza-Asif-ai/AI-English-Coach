"""Runs the REAL CrewAI Agent/Task/Crew with a fake LLM (no network)."""

from crewai import BaseLLM

from app import llm as llm_module
from app import services

from . import samples


class FakeLLM(BaseLLM):
    """Returns canned JSON and remembers the prompt it received."""

    reply: str = ""
    seen: list = []

    def call(self, messages, tools=None, callbacks=None, available_functions=None,
             from_task=None, from_agent=None, response_model=None):
        self.seen.append(messages)
        return self.reply

    def supports_function_calling(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return False


def test_real_crew_generates_reading_exercise(monkeypatch):
    fake = FakeLLM(model="fake-model", reply=samples.as_json(samples.READING), seen=[])
    monkeypatch.setattr(services, "get_llm", lambda: fake)

    exercise = services.generate_exercise("Reading", "Beginner")

    assert exercise["title"] == "A Day at the Market"
    assert len(exercise["questions"]) == 10
    # The prompt (which contains JSON braces) reached the model un-mangled.
    sent = str(fake.seen[0])
    assert '"questions"' in sent and "Beginner" in sent


def test_real_crew_evaluates_writing_with_braces_in_student_text(monkeypatch):
    fake = FakeLLM(model="fake-model", reply=samples.as_json(samples.FEEDBACK), seen=[])
    monkeypatch.setattr(services, "get_llm", lambda: fake)

    result = services.evaluate_writing(
        "Beginner", "My day", "Write.", "I like {curly braces} and I go to school."
    )

    assert result["score"] == 7
    assert "{curly braces}" in str(fake.seen[0])


def test_llm_factory_requires_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    try:
        llm_module.get_llm()
    except llm_module.LLMNotConfigured as error:
        assert "GROQ_API_KEY" in str(error)
    else:
        raise AssertionError("expected LLMNotConfigured")


def test_llm_factory_builds_groq_model(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk_dummy_key")
    monkeypatch.setenv("GROQ_MODEL", "groq/openai/gpt-oss-20b")
    llm_module._build_llm.cache_clear()
    built = llm_module.get_llm()
    assert built.model == "groq/openai/gpt-oss-20b"
    llm_module._build_llm.cache_clear()