from fastapi import FastAPI

from app.config import get_settings
from app.routers import estimations

# Fail fast: valida la configuracion (clave del proveedor, etc.) al arrancar
# el servicio, no en la primera peticion real.
get_settings()

app = FastAPI(
    title="Estimador CAG",
    description=(
        "Servicio que recibe la transcripcion de una reunion y devuelve una "
        "estimacion de software generada por un LLM, con arquitectura CAG "
        "(contexto estatico inyectado en el prompt)."
    ),
    version="0.1.0",
)

app.include_router(estimations.router)


@app.get("/health")
async def health() -> dict:
    """Estado del servicio."""
    return {"status": "ok"}
