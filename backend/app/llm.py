"""LLM setup (Groq through CrewAI/LiteLLM)."""

from functools import lru_cache

from . import config


class LLMNotConfigured(RuntimeError):
    """Raised when GROQ_API_KEY is missing."""


def _patch_cache_breakpoint() -> None:
    """Keep CrewAI's internal `cache_breakpoint` flag out of Groq requests.

    Groq rejects unknown message fields. The patch is optional: if this CrewAI
    version does not have the helper, nothing happens.
    """
    try:
        import crewai.llms.cache as crew_cache

        crew_cache.mark_cache_breakpoint = lambda message: message
    except Exception:  # pragma: no cover - depends on installed crewai
        pass


@lru_cache(maxsize=4)
def _build_llm(api_key: str, model: str, timeout: int):
    from crewai import LLM

    _patch_cache_breakpoint()
    options = {
        "model": f"groq/{model}",
        "api_key": api_key,
        "temperature": 0.6,
        "timeout": timeout,
        # Speed: a short "thinking" phase and a cap on the reply length.
        "max_tokens": config.max_output_tokens(),
    }
    # gpt-oss models accept reasoning_effort; other Groq models do not.
    if "gpt-oss" in model:
        options["reasoning_effort"] = config.reasoning_effort()
    return LLM(**options)


def get_llm():
    api_key = config.groq_api_key()
    if not api_key:
        raise LLMNotConfigured(
            "GROQ_API_KEY is not set. Copy backend/.env.example to "
            "backend/.env, add your Groq key, and restart the backend."
        )
    return _build_llm(api_key, config.groq_model(), config.llm_timeout())