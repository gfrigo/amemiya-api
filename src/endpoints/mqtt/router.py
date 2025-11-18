from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any

from src.core.mqtt import publish_event

router = APIRouter(prefix="/mqtt", tags=["MQTT"])

@router.post("/publish")
def publish_test(company_id: int, device_id: str, payload: dict[str, Any]):
    """Endpoint de teste que publica o payload no tópico de telemetria do device.

    Body esperado: JSON para o `payload`.
    Query/path: `company_id` e `device_id`.
    """
    topic = f"amemiya/{company_id}/device/{device_id}/telemetry"
    try:
        publish_event(topic, payload)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "published", "topic": topic})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
