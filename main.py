from fastapi import FastAPI

from src.core.config import logger
from src.endpoints.attachment.router import router as attachment_router
from src.endpoints.delivery.router import router as delivery_router
from src.endpoints.geopoint.router import router as geopoint_router
from src.endpoints.invoice.router import router as invoice_router
from src.endpoints.login.router import router as login_router
from src.endpoints.maintenance.router import router as maintenance_router
from src.endpoints.refueling.router import router as refueling_router
from src.endpoints.route.router import router as route_router
from src.endpoints.server.router import router as server_router
from src.endpoints.user.router import router as user_router
from src.endpoints.vehicle.router import router as vehicle_router
from src.endpoints.form.router import router as form_router
from src.endpoints.mqtt.router import router as mqtt_router
from src.endpoints.mqtt_auth.router import router as mqtt_auth_router
from src.core.migrations import create_telemetry_table

app = FastAPI()


@app.on_event("startup")
def on_startup():
	# Ensure DB objects required by the services exist
	try:
		create_telemetry_table()
	except Exception:
		# create_telemetry_table logs errors itself
		pass

app.include_router(server_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(attachment_router)
app.include_router(route_router)
app.include_router(geopoint_router)
app.include_router(invoice_router)
app.include_router(maintenance_router)
app.include_router(refueling_router)
app.include_router(delivery_router)
app.include_router(form_router)
app.include_router(mqtt_router)
app.include_router(mqtt_auth_router)