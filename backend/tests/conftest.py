import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Never touch a real key or database during tests.
os.environ.pop("GROQ_API_KEY", None)
os.environ["CREW_VERBOSE"] = "false"

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    yield
