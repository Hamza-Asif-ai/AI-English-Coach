"""Sample AI replies used by the tests."""

import json


def mcq(answer="B", n=1):
    return {
        "question": f"Question {n}: what is 'happy' closest to?",
        "options": {"A": "sad", "B": "glad", "C": "angry", "D": "tired"},
        "answer": answer,
        "explanation": "Glad means happy.",
    }


READING = {
    "title": "A Day at the Market",
    "passage": "Sara goes to the market every Saturday. She buys {fresh} fruit.",
    "questions": [mcq("ABCD"[i % 4], i + 1) for i in range(10)],
}

WRITING = {
    "title": "My Weekend",
    "topic": "Describe your weekend",
    "instructions": "Write about what you do on Saturday and Sunday.",
    "recommended_length": "40 to 60 words",
    "focus": "Present simple",
}

VOCAB = {
    "word": "glad",
    "meaning": "happy about something",
    "part_of_speech": "adjective",
    "example": "I am glad to see you.",
    "synonyms": ["happy", "pleased"],
    "questions": [mcq("ABCD"[i % 4], i + 1) for i in range(10)],
}

GRAMMAR = {
    "topic": "Present simple",
    "rule": "Add -s for he, she and it.",
    "questions": [mcq("ABCD"[i % 4], i + 1) for i in range(10)],
}

FEEDBACK = {
    "score": 7,
    "summary": "Good work.",
    "grammar": "Mostly correct.",
    "vocabulary": "Simple but clear.",
    "spelling_punctuation": "Check capital letters.",
    "structure": "Clear order.",
    "strengths": ["Clear ideas"],
    "improvements": ["Use more linking words"],
    "corrected_version": "I go to school every day.",
    "tip": "Read your text aloud.",
}

BY_AREA = {
    "Reading": READING,
    "Writing": WRITING,
    "Vocabulary": VOCAB,
    "Grammar": GRAMMAR,
}


def as_json(data):
    return json.dumps(data)