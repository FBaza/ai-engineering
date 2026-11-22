# Estimador CAG

Servicio FastAPI que recibe la transcripcion de una reunion con un cliente y devuelve una
estimacion de software generada por un LLM, usando arquitectura **CAG** (Cache/Context
Augmented Generation): el contexto de referencia (ejemplos de estimaciones previas) viaja
integro en el prompt de cada llamada, sin base de datos ni recuperacion.

Ejercicio de la Sesion 2 del Master en AI Engineering (LIDR).

## Estructura

```
estimador-cag-fbaza/
├── app/
│   ├── main.py             # app FastAPI, incluye el router, GET /health
│   ├── config.py           # configuracion (Pydantic BaseSettings)
│   ├── routers/
│   │   └── estimations.py  # POST /api/v1/estimate
│   ├── services/
│   │   └── llm_service.py  # prompt + llamada a Anthropic
│   ├── schemas/
│   │   └── estimation.py   # request/response (Pydantic)
│   └── context/
│       └── examples.py     # ejemplos de estimacion (contexto CAG)
├── transcripcion_ejemplo.md  # transcripcion de ejemplo usada como input de prueba
├── .env.example
└── pyproject.toml
```

## Requisitos

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- Cuenta de Anthropic con credito disponible

## Puesta en marcha

```bash
cd estimador-cag-fbaza
cp .env.example .env
# Editar .env y poner tu ANTHROPIC_API_KEY real

uv sync
uv run uvicorn app.main:app --reload
```

El servicio queda en `http://localhost:8000`, con documentacion Swagger en
`http://localhost:8000/docs`.

## Probar el servicio

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{"transcription": "En la reunion con el equipo de marketing, el cliente explico que necesita una landing page con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en Figma."}'
```

Ver `transcripcion_ejemplo.md` para otro ejemplo de transcripcion de entrada.

## Notas de arquitectura

- `routers/` solo valida y delega: no construye prompts ni llama al LLM.
- `services/` contiene la logica: construir el system prompt con los ejemplos
  de `context/`, llamar a Anthropic, devolver el resultado.
- `context/` es hoy estatico; es el punto de sustitucion limpio hacia RAG en
  modulos posteriores del programa.
- La API key nunca va en el codigo: se carga desde `.env` (en `.gitignore`).
