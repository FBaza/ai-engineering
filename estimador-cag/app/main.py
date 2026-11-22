from fastapi import FastAPI

from app.routers import estimations

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
