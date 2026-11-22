"""Contexto estatico para la arquitectura CAG.

Estas estimaciones de ejemplo viajan en cada llamada al LLM, dentro del
system prompt (ver app/services/llm_service.py). Hacen de "few-shot
examples": le muestran al modelo el nivel de detalle y el formato que
esperamos en una estimacion nueva. El dia que esto no quepa en la ventana
de contexto, este modulo es el punto de sustitucion hacia RAG.
"""

ESTIMATION_EXAMPLES = [
    {
        "meeting_summary": (
            "El cliente, una gestoria pequena, necesita digitalizar la recepcion de "
            "documentos de sus clientes. Piden un portal web donde el cliente final "
            "suba facturas y nominas en PDF, un area interna donde el gestor las "
            "clasifique por tipo y periodo, y notificaciones por email cuando falta "
            "documentacion de un mes. No hace falta app movil, solo web responsive. "
            "Tienen ya un dominio y alojamiento, pero ninguna base de datos."
        ),
        "estimation": """
## Estimacion: Portal de Documentacion para Gestoria

### Desglose de tareas:
1. Diseno de modelo de datos y autenticacion (clientes + gestores): 16 horas (880 EUR)
2. Area de cliente: subida y listado de documentos: 24 horas (1.320 EUR)
3. Area interna: clasificacion y revision de documentos: 28 horas (1.540 EUR)
4. Notificaciones por email (documentacion pendiente): 12 horas (660 EUR)
5. Despliegue inicial en el alojamiento existente: 8 horas (440 EUR)
6. Pruebas y correccion de errores: 16 horas (880 EUR)

**Total estimado: 104 horas (5.720 EUR, a 55 EUR/hora)**
**Equipo recomendado: 1 desarrollador full-stack**
**Duracion estimada: 4-5 semanas**
""",
    },
    {
        "meeting_summary": (
            "Un centro de formacion online quiere automatizar la generacion de "
            "certificados de sus alumnos al terminar un curso. El sistema debe "
            "escuchar un evento de 'curso completado' desde su plataforma actual "
            "(via webhook), generar un PDF con una plantilla de certificado, y "
            "enviarlo por email al alumno. Tambien quieren un listado interno de "
            "certificados emitidos, consultable por nombre o curso."
        ),
        "estimation": """
## Estimacion: Generador Automatico de Certificados

### Desglose de tareas:
1. Endpoint receptor del webhook de 'curso completado': 8 horas (440 EUR)
2. Generacion de PDF a partir de plantilla (datos del alumno/curso): 16 horas (880 EUR)
3. Envio de email con el certificado adjunto: 8 horas (440 EUR)
4. Listado interno de certificados emitidos, con busqueda: 14 horas (770 EUR)
5. Pruebas end-to-end con la plataforma del cliente: 10 horas (550 EUR)

**Total estimado: 56 horas (3.080 EUR, a 55 EUR/hora)**
**Equipo recomendado: 1 desarrollador backend**
**Duracion estimada: 2-3 semanas**
""",
    },
]


def format_examples_for_prompt(examples: list[dict]) -> str:
    """Convierte los ejemplos en texto plano para inyectar en el system prompt."""
    bloques = []
    for i, ejemplo in enumerate(examples, start=1):
        bloques.append(
            f"--- EJEMPLO {i} ---\n"
            f"Resumen de la reunion:\n{ejemplo['meeting_summary']}\n\n"
            f"Estimacion generada:\n{ejemplo['estimation']}"
        )
    return "\n\n".join(bloques)
