"""HTTP API (all routes live under /api)."""

import logging

from fastapi import APIRouter, HTTPException, Query

from . import config, db, services
from .llm import LLMNotConfigured
from .schemas import (
    CLIENT_ID_PATTERN,
    ExerciseRequest,
    ExerciseResponse,
    ProgressSaveRequest,
    WritingRequest,
    WritingResponse,
)

logger = logging.getLogger("ai_english_coach")

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "healthy", "llm_configured": bool(config.groq_api_key())}


@router.post("/generate-exercise", response_model=ExerciseResponse)
def generate_exercise(request: ExerciseRequest):
    session_id = request.session_id or services.new_session_id()
    try:
        exercise = services.generate_exercise(request.area, request.level)
    except LLMNotConfigured as error:
        raise HTTPException(status_code=503, detail=str(error))
    except services.GenerationError as error:
        logger.warning("Exercise generation failed: %s", error)
        raise HTTPException(status_code=502, detail=str(error))
    return ExerciseResponse(
        level=request.level,
        area=request.area,
        session_id=session_id,
        exercise=exercise,
    )


@router.post("/evaluate-writing", response_model=WritingResponse)
def evaluate_writing(request: WritingRequest):
    try:
        feedback = services.evaluate_writing(
            request.level, request.topic, request.instructions, request.answer
        )
    except LLMNotConfigured as error:
        raise HTTPException(status_code=503, detail=str(error))
    except services.GenerationError as error:
        logger.warning("Writing evaluation failed: %s", error)
        raise HTTPException(status_code=502, detail=str(error))
    return WritingResponse(level=request.level, feedback=feedback)


@router.post("/progress")
def save_progress(request: ProgressSaveRequest):
    db.save_result(request.client_id, request.area, request.level, request.score, request.total)
    return {"success": True, **db.get_stats(request.client_id)}


@router.get("/progress")
def get_progress(client_id: str = Query(pattern=CLIENT_ID_PATTERN)):
    return {"success": True, **db.get_stats(client_id)}
