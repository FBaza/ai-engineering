from pydantic import BaseModel, Field


class EstimationRequest(BaseModel):
    """Peticion de estimacion: la transcripcion de una reunion con el cliente."""

    transcription: str = Field(..., min_length=20, description="Transcripcion de la reunion a estimar")


class EstimationResponse(BaseModel):
    """Estimacion generada por el LLM, con metadatos de la llamada."""

    estimation: str = Field(..., description="Estimacion generada, en markdown")
    model: str = Field(..., description="Modelo del LLM usado")
    provider: str = Field(..., description="Proveedor del LLM usado")
