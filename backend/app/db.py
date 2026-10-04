"""SQLite storage for practice results (anonymous client_id, no login)."""

import sqlite3
from collections import defaultdict
from contextlib import closing
from datetime import date, datetime, timedelta, timezone

from . import config
from .schemas import AREAS


def _connect() -> sqlite3.Connection:
    path = config.database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                area TEXT NOT NULL,
                level TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_results_client ON results (client_id, created_at)"
        )


def save_result(client_id: str, area: str, level: str, score: int, total: int) -> None:
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(_connect()) as connection, connection:
        connection.execute(
            "INSERT INTO results (client_id, area, level, score, total, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (client_id, area, level, score, total, created_at),
        )


def _streak(days: set[date], today: date) -> int:
    """Consecutive practice days ending today (or yesterday)."""
    if today in days:
        cursor = today
    elif (today - timedelta(days=1)) in days:
        cursor = today - timedelta(days=1)
    else:
        return 0
    count = 0
    while cursor in days:
        count += 1
        cursor -= timedelta(days=1)
    return count


def get_stats(client_id: str) -> dict:
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT area, level, score, total, created_at FROM results "
            "WHERE client_id = ? ORDER BY id ASC",
            (client_id,),
        ).fetchall()

    per_area = {area: {"count": 0, "average": 0} for area in AREAS}
    percents: dict[str, list[float]] = defaultdict(list)
    days: set[date] = set()
    all_percents: list[float] = []

    for row in rows:
        percent = row["score"] / row["total"] * 100
        percents[row["area"]].append(percent)
        all_percents.append(percent)
        days.add(datetime.fromisoformat(row["created_at"]).date())

    for area, values in percents.items():
        if area in per_area:
            per_area[area] = {
                "count": len(values),
                "average": round(sum(values) / len(values)),
            }

    recent = [
        {
            "area": row["area"],
            "level": row["level"],
            "score": row["score"],
            "total": row["total"],
            "percent": round(row["score"] / row["total"] * 100),
            "created_at": row["created_at"],
        }
        for row in reversed(rows[-5:])
    ]

    today = datetime.now(timezone.utc).date()
    return {
        "total_practices": len(rows),
        "average_score": round(sum(all_percents) / len(all_percents)) if all_percents else 0,
        "streak": _streak(days, today),
        "per_area": per_area,
        "recent": recent,
        "recommendation": _recommend(per_area),
    }


def _recommend(per_area: dict) -> dict:
    """Simple coach logic: untried area first, otherwise the weakest area."""
    for area in AREAS:
        if per_area[area]["count"] == 0:
            return {"area": area, "reason": f"You have not tried {area} yet."}
    weakest = min(AREAS, key=lambda a: per_area[a]["average"])
    average = per_area[weakest]["average"]
    return {
        "area": weakest,
        "reason": f"{weakest} is your lowest area ({average}% average). Practise it next.",
    }
