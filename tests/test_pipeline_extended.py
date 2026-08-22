# -*- coding: utf-8 -*-
"""Extended pytest suite for the Interview Coach pipeline.

This file adds explicit, deterministic checks for the core behaviours that the
original ad‑hoc test (test_cases.py) only exercised without assertions.
"""

import sqlite3
from pathlib import Path

import pytest

# Import the functions we need from the project
from ai.feedback_engine import get_next_difficulty, get_missing_concepts
from ai.scorer import score_answer

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _db_path() -> str:
    """Return the absolute path to the project's SQLite database.
    Mirrors the internal logic used by the modules.
    """
    base_dir = Path(__file__).resolve().parents[1]
    db_path = base_dir / "database.db"
    if not db_path.exists():
        db_path = Path("database.db")
    return str(db_path)

def _question_id(search_term: str) -> int:
    """Lookup a question ID by a substring of its text.
    Returns the first matching ID or raises ValueError if none found.
    """
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("SELECT id FROM Questions WHERE question_text LIKE ?", (f"%{search_term}%",))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    raise ValueError(f"No question found containing '{search_term}'")

# ---------------------------------------------------------------------------
# 1. Adaptive‑difficulty behaviour
# ---------------------------------------------------------------------------

def test_adaptive_difficulty_increases_on_good_score():
    assert get_next_difficulty("Easy", "Good") == "Medium"
    assert get_next_difficulty("Medium", "Excellent") == "Hard"
    # Already at Hard – should stay Hard
    assert get_next_difficulty("Hard", "Excellent") == "Hard"


def test_adaptive_difficulty_decreases_on_poor_score():
    assert get_next_difficulty("Hard", "Poor") == "Medium"
    assert get_next_difficulty("Medium", "Average") == "Easy"
    # Already at Easy – should stay Easy
    assert get_next_difficulty("Easy", "Poor") == "Easy"

# ---------------------------------------------------------------------------
# 2. Scoring correctness for known strong / weak answers
# ---------------------------------------------------------------------------

def test_known_strong_answer_scores_good_or_excellent():
    # Question 110 (Denormalization) has an "Excellent" reference answer.
    strong_answer = (
        "Denormalization duplicates data to avoid joins, improving read performance "
        "but risking consistency issues. It’s a trade‑off between speed and storage."
    )
    label, _ = score_answer(_question_id('denormal'), strong_answer)
    # The model may give "Excellent" or "Good" – both are acceptable for a strong answer.
    assert label in ("Excellent", "Good"), f"Unexpected label: {label}"


def test_known_weak_answer_scores_poor():
    weak_answer = "I don't know."
    label, _ = score_answer(_question_id('denormal'), weak_answer)
    assert label == "Poor", f"Weak answer should be Poor, got {label}"

# ---------------------------------------------------------------------------
# 3. Missing‑concept detection
# ---------------------------------------------------------------------------

def test_missing_concepts_empty_for_strong_answer():
    strong_answer = (
        "Denormalization duplicates data to avoid joins, improving read performance "
        "but risking consistency issues. It’s a trade‑off between speed and storage."
    )
    missing = get_missing_concepts(_question_id('denormal'), strong_answer)
    assert missing == [] or len(missing) == 0


def test_missing_concepts_nonempty_for_weak_answer():
    weak_answer = "I store data in a single table."
    missing = get_missing_concepts(_question_id('denormal'), weak_answer)
    assert len(missing) >= 1, "Weak answer should miss at least one concept"

# ---------------------------------------------------------------------------
# 4. Job‑role distribution sanity check
# ---------------------------------------------------------------------------

def test_job_role_distribution_correct():
    # The DB stores the role directly in the Questions table (job_role column).
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("SELECT job_role, COUNT(*) FROM Questions GROUP BY job_role")
    rows = cur.fetchall()
    conn.close()
    role_counts = {role: cnt for role, cnt in rows}
    # Expected counts (may vary slightly if the seed data changed, allow ±2)
    assert role_counts.get("Software Engineer") in (104, 105, 106), \
        f"Software Engineer count unexpected: {role_counts.get('Software Engineer')}"
    assert role_counts.get("General/HR") in (39, 40, 41), \
        f"General/HR count unexpected: {role_counts.get('General/HR')}"
    total = sum(role_counts.values())
    assert total in (144, 145, 146), f"Total role count unexpected: {total}"
    # Verify approximate ratio (tolerance 10%)
    if role_counts.get("Software Engineer") and role_counts.get("General/HR"):
        ratio = role_counts["Software Engineer"] / role_counts["General/HR"]
        expected = 105 / 40
        assert abs(ratio - expected) / expected < 0.1, "Role ratio deviates >10%"

# ---------------------------------------------------------------------------
# 5. No duplicate question text
# ---------------------------------------------------------------------------

def test_no_duplicate_question_text():
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("SELECT question_text FROM Questions")
    texts = [row[0] for row in cur.fetchall()]
    conn.close()
    assert len(texts) == len(set(texts)), "Duplicate question texts detected"

def test_scoring_handles_empty_answer():
    label, _ = score_answer(_question_id('denormal'), "")
    assert label in ("Poor", "Average", "Good", "Excellent")

# ---------------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------------
