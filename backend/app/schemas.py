"""Pydantic models: API requests/responses and validated AI output."""

import re
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)

Level = Literal["Beginner", "Intermediate", "Advanced"]
Area = Literal["Reading", "Writing", "Vocabulary", "Grammar"]

AREAS: tuple[str, ...] = ("Reading", "Writing", "Vocabulary", "Grammar")
LETTERS = ("A", "B", "C", "D")
QUESTION_COUNT = 10

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def _snake(key: str) -> str:
    key = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", str(key).strip())
    return re.sub(r"[\s\-]+", "_", key).lower()


class AIModel(BaseModel):
    """Base for AI output: tolerant key names (camelCase / spaces) and numbers."""

    model_config = ConfigDict(coerce_numbers_to_str=True, extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def _normalize_keys(cls, data):
        if isinstance(data, dict):
            return {_snake(k): v for k, v in data.items()}
        return data


def _to_list(value):
    """Accept a list or a comma/semicolon/newline separated string."""
    if isinstance(value, str):
        parts = re.split(r"[\n;,]+", value)
        return [p.strip(" -•*\t") for p in parts if p.strip(" -•*\t")]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return value


# ---------------------------------------------------------------- exercises


_VAGUE_OPTION = re.compile(
    r"\b(all|none|neither|both)\s+of\s+(the\s+)?(above|these|them)\b"
    r"|\b(both|all)\s+[a-d]\s*(and|&)\s*[a-d]\b"
    r"|^\s*(a|b|c|d)\s+and\s+(a|b|c|d)\s*$",
    re.IGNORECASE,
)


def _plain(text: str) -> str:
    """Lower-case text with single spaces, used to compare options.

    Punctuation is kept on purpose: in grammar, two options may differ only by
    a comma or an apostrophe and still be a valid, different choice.
    """
    return re.sub(r"\s+", " ", text.lower()).strip()


class MCQ(AIModel):
    question: Text
    options: dict[str, Text]
    answer: Literal["A", "B", "C", "D"]
    explanation: str = ""

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data):
        if not isinstance(data, dict):
            return data
        data = {_snake(k): v for k, v in data.items()}

        options = data.get("options")
        if isinstance(options, list):
            options = {LETTERS[i]: v for i, v in enumerate(options[:4])}
        if isinstance(options, dict):
            cleaned = {}
            for key, value in options.items():
                letter = str(key).strip().upper()[:1]
                text = str(value).strip()
                # remove a leading "A. " / "B) " the AI may have added to the text
                text = re.sub(r"^\(?[A-Da-d][\.\):]\s+", "", text)
                cleaned[letter] = text
            options = cleaned
        data["options"] = options

        answer = data.get("answer", data.get("correct_answer"))
        if isinstance(answer, str) and isinstance(options, dict):
            match = re.match(r"\s*([A-Da-d])(?![A-Za-z])", answer)
            if match:
                answer = match.group(1).upper()
            else:
                for letter, text in options.items():
                    if text.strip().lower() == answer.strip().lower():
                        answer = letter
                        break
        data["answer"] = answer
        return data

    @field_validator("options")
    @classmethod
    def _check_options(cls, value):
        if set(value) != set(LETTERS):
            raise ValueError("options must contain exactly A, B, C and D")
        if any(not v for v in value.values()):
            raise ValueError("options must not be empty")
        if len({_plain(v) for v in value.values()}) != 4:
            raise ValueError("options must be different from each other")
        for text in value.values():
            if _VAGUE_OPTION.search(text):
                raise ValueError(
                    "options must not be 'all/none of the above' or 'both X and Y'"
                )
        return value


def _ten_questions(value):
    """Keep the valid, different questions and return exactly QUESTION_COUNT of them.

    The AI is asked for a few extra questions, so one broken question (duplicate
    options, bad answer letter, repeated question) is dropped instead of
    rejecting the whole exercise.
    """
    if isinstance(value, dict):  # a single question instead of a list
        value = [value]
    if not isinstance(value, list):
        raise ValueError(f"exactly {QUESTION_COUNT} questions are required")
    good, seen = [], set()
    for item in value:
        try:
            question = MCQ.model_validate(item)
        except ValidationError:
            continue
        key = question.question.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        good.append(question)
    if len(good) < QUESTION_COUNT:
        raise ValueError(
            f"only {len(good)} valid different questions, {QUESTION_COUNT} are required"
        )
    return good[:QUESTION_COUNT]


def _unique_questions(items):
    texts = [q.question.strip().lower() for q in items]
    if len(set(texts)) != len(texts):
        raise ValueError("questions must be different from each other")
    return items


class ReadingExercise(AIModel):
    title: Text
    passage: Text
    questions: list[MCQ]

    @field_validator("questions", mode="before")
    @classmethod
    def _count(cls, value):
        return _ten_questions(value)

    @field_validator("questions")
    @classmethod
    def _unique(cls, value):
        return _unique_questions(value)


class WritingExercise(AIModel):
    title: Text
    topic: Text
    instructions: Text
    recommended_length: Text
    focus: Text


class VocabularyExercise(AIModel):
    word: Text
    meaning: Text
    part_of_speech: Text
    example: Text
    synonyms: list[Text]
    questions: list[MCQ]

    @model_validator(mode="before")
    @classmethod
    def _old_single_question(cls, data):
        # tolerate an AI that still returns one "question" key
        if isinstance(data, dict):
            data = {_snake(k): v for k, v in data.items()}
            if "questions" not in data and "question" in data:
                data["questions"] = data.pop("question")
        return data

    @field_validator("questions", mode="before")
    @classmethod
    def _count(cls, value):
        return _ten_questions(value)

    @field_validator("questions")
    @classmethod
    def _unique(cls, value):
        return _unique_questions(value)

    @field_validator("synonyms", mode="before")
    @classmethod
    def _synonyms(cls, value):
        value = _to_list(value)
        if not value:
            raise ValueError("at least one synonym is required")
        return value[:4]


class GrammarExercise(AIModel):
    topic: Text
    rule: Text
    questions: list[MCQ]

    @model_validator(mode="before")
    @classmethod
    def _old_single_question(cls, data):
        if isinstance(data, dict):
            data = {_snake(k): v for k, v in data.items()}
            if "questions" not in data and "question" in data:
                data["questions"] = data.pop("question")
        return data

    @field_validator("questions", mode="before")
    @classmethod
    def _count(cls, value):
        return _ten_questions(value)

    @field_validator("questions")
    @classmethod
    def _unique(cls, value):
        return _unique_questions(value)


class WritingFeedback(AIModel):
    score: int
    summary: Text
    grammar: Text
    vocabulary: Text
    spelling_punctuation: Text
    structure: Text
    strengths: list[Text]
    improvements: list[Text]
    corrected_version: Text
    tip: Text

    @field_validator("score", mode="before")
    @classmethod
    def _score(cls, value):
        if isinstance(value, str):
            match = re.search(r"\d+(?:\.\d+)?", value)
            if not match:
                raise ValueError("score must be a number")
            value = float(match.group())
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("score must be a number")
        return max(0, min(10, round(value)))

    @field_validator("strengths", "improvements", mode="before")
    @classmethod
    def _lists(cls, value):
        value = _to_list(value)
        if not value:
            raise ValueError("at least one item is required")
        return value[:6]


EXERCISE_MODELS: dict[str, type[AIModel]] = {
    "Reading": ReadingExercise,
    "Writing": WritingExercise,
    "Vocabulary": VocabularyExercise,
    "Grammar": GrammarExercise,
}


# ------------------------------------------------------------ API contracts


class ExerciseRequest(BaseModel):
    level: Level = "Beginner"
    area: Area = "Reading"
    session_id: str = Field(default="", max_length=100)


class ExerciseResponse(BaseModel):
    level: Level
    area: Area
    session_id: str
    exercise: dict


class WritingRequest(BaseModel):
    level: Level = "Beginner"
    topic: str = Field(min_length=1, max_length=500)
    instructions: str = Field(default="", max_length=1500)
    answer: str = Field(min_length=10, max_length=6000)


class WritingResponse(BaseModel):
    level: Level
    feedback: dict


CLIENT_ID_PATTERN = r"^[A-Za-z0-9_-]{8,64}$"


class ProgressSaveRequest(BaseModel):
    client_id: str = Field(pattern=CLIENT_ID_PATTERN)
    area: Area
    level: Level
    score: int = Field(ge=0, le=100)
    total: int = Field(gt=0, le=100)

    @model_validator(mode="after")
    def _score_within_total(self):
        if self.score > self.total:
            raise ValueError("score cannot be greater than total")
        return self