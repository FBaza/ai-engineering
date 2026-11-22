"""Logica de negocio: construir el prompt CAG y llamar al LLM.

Arquitectura CAG: el contexto (ejemplos de estimaciones previas) se inyecta
integro en el system prompt de cada llamada. No hay base de datos ni
recuperacion: todo el "conocimiento" del sistema viaja en el propio mensaje.

Soporta dos proveedores (Anthropic y OpenAI), seleccionables con LLM_PROVIDER.
"""

from app.config import Settings, get_settings
from app.context.examples import ESTIMATION_EXAMPLES, format_examples_for_prompt

# 2000-4000 tokens recomendado para estimaciones (ver apunte de arquitectura de
# conversaciones): por debajo de eso la respuesta puede quedar truncada.
MAX_TOKENS = 3000


class LLMServiceError(Exception):
    """Error al llamar al proveedor del LLM."""


def build_system_prompt() -> str:
    """Construye el system prompt: rol, formato esperado y ejemplos de contexto (CAG).

    Orden deliberado (ver apunte de gestion de contexto): el formato de
    salida esperado se especifica antes de los ejemplos, y la transcripcion
    del usuario llega aparte, como ultimo mensaje.
    """
    ejemplos = format_examples_for_prompt(ESTIMATION_EXAMPLES)
    return (
        "Eres un estimador de software experto, con anos de experiencia "
        "calculando presupuestos de proyectos a partir de reuniones con clientes.\n\n"
        "IMPORTANTE: nunca respondas pidiendo mas informacion. Si la "
        "transcripcion es breve o ambigua, haz las asunciones razonables que "
        "haria un consultor senior (indicalas brevemente al final, bajo "
        "'Supuestos') y genera igualmente la estimacion completa.\n\n"
        "A partir de la transcripcion de una reunion que te enviara el usuario, "
        "genera una estimacion con este formato: un titulo, un desglose de "
        "tareas con horas y coste, el total de horas y coste, el equipo "
        "recomendado y la duracion estimada.\n\n"
        "A continuacion tienes ejemplos de estimaciones previas. Usalos como "
        "referencia de formato, nivel de detalle y criterio para desglosar "
        "tareas:\n\n"
        f"{ejemplos}"
    )


def generate_estimation(transcription: str) -> dict:
    """Llama al LLM configurado y devuelve la estimacion junto con sus metadatos."""
    settings = get_settings()

    if settings.LLM_PROVIDER == "anthropic":
        return _call_anthropic(settings, transcription)
    if settings.LLM_PROVIDER == "openai":
        return _call_openai(settings, transcription)
    raise LLMServiceError(f"Proveedor no soportado: {settings.LLM_PROVIDER}")


def _call_anthropic(settings: Settings, transcription: str) -> dict:
    from anthropic import Anthropic

    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    try:
        response = client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=MAX_TOKENS,
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


def _call_openai(settings: Settings, transcription: str) -> dict:
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": build_system_prompt()},
                {"role": "user", "content": transcription},
            ],
        )
    except Exception as exc:
        raise LLMServiceError(f"Fallo en la llamada a OpenAI: {exc}") from exc

    return {
        "estimation": response.choices[0].message.content,
        "model": response.model,
        "provider": "openai",
    }
