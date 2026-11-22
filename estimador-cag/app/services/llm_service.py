"""Logica de negocio: construir el prompt CAG y llamar al LLM.

Arquitectura CAG: el contexto (ejemplos de estimaciones previas) se inyecta
integro en el system prompt de cada llamada. No hay base de datos ni
recuperacion: todo el "conocimiento" del sistema viaja en el propio mensaje.
"""

from anthropic import Anthropic

from app.config import get_settings
from app.context.examples import ESTIMATION_EXAMPLES, format_examples_for_prompt


class LLMServiceError(Exception):
    """Error al llamar al proveedor del LLM."""


def build_system_prompt() -> str:
    """Construye el system prompt: rol del modelo + ejemplos de contexto (CAG)."""
    ejemplos = format_examples_for_prompt(ESTIMATION_EXAMPLES)
    return (
        "Eres un estimador de software experto, con anos de experiencia "
        "calculando presupuestos de proyectos a partir de reuniones con clientes.\n\n"
        "A continuacion tienes ejemplos de estimaciones previas. Usalos como "
        "referencia de formato, nivel de detalle y criterio para desglosar tareas "
        "en horas:\n\n"
        f"{ejemplos}\n\n"
        "Ahora, a partir de la transcripcion de una nueva reunion que te va a "
        "enviar el usuario, genera una estimacion con el mismo formato: un "
        "titulo, un desglose de tareas con horas, el total de horas, el equipo "
        "recomendado y la duracion estimada."
    )


def generate_estimation(transcription: str) -> dict:
    """Llama al LLM configurado y devuelve la estimacion junto con sus metadatos."""
    settings = get_settings()

    if settings.LLM_PROVIDER != "anthropic":
        raise LLMServiceError(f"Proveedor no soportado: {settings.LLM_PROVIDER}")

    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=1500,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": transcription}],
        )
    except Exception as exc:
        raise LLMServiceError(f"Fallo en la llamada a Anthropic: {exc}") from exc

    return {
        "estimation": response.content[0].text,
        "model": response.model,
        "provider": "anthropic",
    }
