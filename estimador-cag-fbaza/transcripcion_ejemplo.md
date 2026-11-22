# Transcripcion de ejemplo (input de prueba)

Transcripcion ficticia usada como parametro de entrada para probar el endpoint `POST /api/v1/estimate`.

---

En la reunion con el equipo de marketing, el cliente explico que necesita una landing page
con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion de blog
con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en
Figma.

---

## Como usarla

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{"transcription": "En la reunion con el equipo de marketing, el cliente explico que necesita una landing page con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en Figma."}'
```
