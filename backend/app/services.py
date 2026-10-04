"""Runs CrewAI agents and returns validated results."""

import json
import re
import uuid

from pydantic import ValidationError

from . import config
from .agents import build_agent
from .llm import LLMNotConfigured, get_llm
from .prompts import PROMPT_BUILDERS, writing_feedback_prompt
from .schemas import EXERCISE_MODELS, WritingFeedback

EXPECTED_OUTPUT = (
    "A single valid JSON object that follows the structure described in the task. "
    "No Markdown and no extra text."
)


class GenerationError(RuntimeError):
    """The AI did not return a usable result after all attempts."""


def run_crew(area: str, prompt: str) -> str:
    """Run one agent/task/crew and return the raw text answer."""
    from crewai import Crew, Process, Task

    llm = get_llm()
    agent = build_agent(area, llm, verbose=config.crew_verbose())
    task = Task(description=prompt, expected_output=EXPECTED_OUTPUT, agent=agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=config.crew_verbose(),
    )
    result = crew.kickoff()
    return str(getattr(result, "raw", None) or result)


def extract_json(text: str) -> dict:
    """Pull a JSON object out of an AI reply (tolerates code fences / extra text)."""
    cleaned = (text or "").strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", cleaned).strip()
    try:
        data = json.loads(cleaned)
    except ValueError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start == -1 or end <= start:
            raise ValueError("The reply does not contain a JSON object.")
        data = json.loads(cleaned[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("The reply is not a JSON object.")
    return data


def _short_error(error: Exception) -> str:
    if isinstance(error, ValidationError):
        parts = []
        for item in error.errors()[:3]:
            location = ".".join(str(p) for p in item["loc"]) or "reply"
            parts.append(f"{location}: {item['msg']}")
        return "; ".join(parts)
    return str(error)[:200]


def _run_validated(area: str, prompt: str, model) -> dict:
    last_error = "unknown error"
    current_prompt = prompt
    for _ in range(config.max_attempts()):
        try:
            raw = run_crew(area, current_prompt)
            data = extract_json(raw)
            return model.model_validate(data).model_dump()
        except LLMNotConfigured:
            raise
        except Exception as error:  # network, auth, bad JSON, bad structure
            last_error = _short_error(error)
            current_prompt = (
                f"{prompt}\n\nIMPORTANT: your previous reply was rejected ({last_error}). "
                "Reply again with ONLY the valid JSON object in the required structure."
            )
    raise GenerationError(
        f"The AI could not produce a valid result ({last_error}). Please try again."
    )


def generate_exercise(area: str, level: str) -> dict:
    prompt = PROMPT_BUILDERS[area](level)
    return _run_validated(area, prompt, EXERCISE_MODELS[area])


def evaluate_writing(level: str, topic: str, instructions: str, answer: str) -> dict:
    prompt = writing_feedback_prompt(level, topic, instructions, answer)
    return _run_validated("Writing", prompt, WritingFeedback)


def new_session_id() -> str:
    return uuid.uuid4().hex
