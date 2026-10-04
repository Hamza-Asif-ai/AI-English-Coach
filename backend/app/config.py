"""Central configuration. Importing this module loads backend/.env."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Must be set before crewai is imported anywhere: no telemetry network calls.
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "").strip()


def groq_model() -> str:
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    if model.startswith("groq/"):
        model = model[len("groq/"):]
    return model or "openai/gpt-oss-20b"


def llm_timeout() -> int:
    return _int_env("LLM_TIMEOUT", 90)


def max_attempts() -> int:
    return max(1, _int_env("LLM_MAX_ATTEMPTS", 3))


def reasoning_effort() -> str:
    """How long the model 'thinks' before answering. 'low' = much faster."""
    value = os.getenv("GROQ_REASONING_EFFORT", "low").strip().lower()
    return value if value in {"low", "medium", "high"} else "low"


def max_output_tokens() -> int:
    return max(1500, _int_env("LLM_MAX_TOKENS", 5000))


def crew_verbose() -> bool:
    return os.getenv("CREW_VERBOSE", "false").strip().lower() in {"1", "true", "yes"}


def database_path() -> Path:
    raw = os.getenv("DATABASE_PATH", "").strip()
    return Path(raw) if raw else BASE_DIR / "data" / "progress.db"


def cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "")
    return [item.strip().rstrip("/") for item in raw.split(",") if item.strip()]