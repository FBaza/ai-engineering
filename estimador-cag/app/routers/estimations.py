from fastapi import APIRouter, HTTPException

from app.schemas.estimation import EstimationRequest, EstimationResponse
from app.services.llm_service import LLMServiceError, generate_estimation

router = APIRouter(prefix="/api/v1", tags=["estimations"])


@router.post("/estimate", response_model=EstimationResponse)
async def create_estimation(request: EstimationRequest) -> EstimationResponse:
    """Recibe la transcripcion de una reunion y devuelve una estimacion generada por el LLM."""
    try:
        resultado = generate_estimation(request.transcription)
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return EstimationResponse(**resultado)
