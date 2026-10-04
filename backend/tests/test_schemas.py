import pytest
from pydantic import ValidationError

from app.schemas import (
    MCQ,
    GrammarExercise,
    ReadingExercise,
    VocabularyExercise,
    WritingFeedback,
)
from app.services import extract_json

from . import samples


def test_mcq_accepts_list_options_and_answer_text():
    item = MCQ.model_validate(
        {
            "question": "Pick one",
            "options": ["one", "two", "three", "four"],
            "answer": "three",
            "explanation": "x",
        }
    )
    assert item.answer == "C"
    assert item.options["D"] == "four"


def test_mcq_answer_with_dot_and_lowercase():
    item = MCQ.model_validate({**samples.mcq(), "answer": "b. glad"})
    assert item.answer == "B"


def test_mcq_rejects_duplicate_options():
    bad = samples.mcq()
    bad["options"]["C"] = "sad"
    with pytest.raises(ValidationError):
        MCQ.model_validate(bad)


def test_mcq_rejects_all_of_the_above_and_punctuation_duplicates():
    bad = samples.mcq()
    bad["options"]["D"] = "All of the above"
    with pytest.raises(ValidationError):
        MCQ.model_validate(bad)
    dup = samples.mcq()
    dup["options"]["C"] = "SAD"
    with pytest.raises(ValidationError):
        MCQ.model_validate(dup)


def test_mcq_allows_options_that_differ_only_by_punctuation():
    item = MCQ.model_validate(
        {
            "question": "Which sentence is punctuated correctly?",
            "options": {
                "A": "Having finished, she left.",
                "B": "Having finished she left.",
                "C": "Having finished; she left.",
                "D": "Having, finished she left.",
            },
            "answer": "A",
        }
    )
    assert item.answer == "A"


def test_one_broken_question_is_dropped_when_a_spare_exists():
    data = dict(samples.GRAMMAR)
    broken = samples.mcq(n=99)
    broken["options"]["C"] = broken["options"]["A"]  # duplicate options
    data["questions"] = [broken] + samples.GRAMMAR["questions"]
    assert len(GrammarExercise.model_validate(data).questions) == 10


def test_mcq_rejects_missing_option():
    bad = samples.mcq()
    del bad["options"]["D"]
    with pytest.raises(ValidationError):
        MCQ.model_validate(bad)


def test_mcq_strips_letter_prefix_from_options():
    data = samples.mcq()
    data["options"] = {"A": "A. sad", "B": "B) glad", "C": "C: angry", "D": "tired"}
    item = MCQ.model_validate(data)
    assert item.options == {"A": "sad", "B": "glad", "C": "angry", "D": "tired"}


def test_reading_needs_ten_questions_and_truncates_extra():
    data = dict(samples.READING)
    data["questions"] = data["questions"][:9]
    with pytest.raises(ValidationError):
        ReadingExercise.model_validate(data)
    data["questions"] = samples.READING["questions"] + [samples.mcq(n=11)]
    assert len(ReadingExercise.model_validate(data).questions) == 10


@pytest.mark.parametrize(
    ("model", "sample"),
    [(VocabularyExercise, samples.VOCAB), (GrammarExercise, samples.GRAMMAR)],
)
def test_vocab_and_grammar_need_ten_questions(model, sample):
    assert len(model.model_validate(sample).questions) == 10
    short = {**sample, "questions": sample["questions"][:5]}
    with pytest.raises(ValidationError):
        model.model_validate(short)


def test_duplicate_questions_are_rejected():
    data = dict(samples.GRAMMAR)
    data["questions"] = [samples.mcq()] * 10
    with pytest.raises(ValidationError):
        GrammarExercise.model_validate(data)


def test_camel_case_keys_and_string_synonyms():
    data = dict(samples.VOCAB)
    data["partOfSpeech"] = data.pop("part_of_speech")
    data["synonyms"] = "happy, pleased; cheerful"
    item = VocabularyExercise.model_validate(data)
    assert item.part_of_speech == "adjective"
    assert item.synonyms == ["happy", "pleased", "cheerful"]


def test_feedback_score_is_clamped_and_parsed():
    assert WritingFeedback.model_validate({**samples.FEEDBACK, "score": "8/10"}).score == 8
    assert WritingFeedback.model_validate({**samples.FEEDBACK, "score": 14}).score == 10
    assert WritingFeedback.model_validate({**samples.FEEDBACK, "score": 6.6}).score == 7


def test_extract_json_variants():
    assert extract_json('{"a": 1}') == {"a": 1}
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert extract_json('Here you go:\n{"a": {"b": 2}}\nThanks!') == {"a": {"b": 2}}
    with pytest.raises(ValueError):
        extract_json("no json here")
    with pytest.raises(ValueError):
        extract_json("[1, 2, 3]")