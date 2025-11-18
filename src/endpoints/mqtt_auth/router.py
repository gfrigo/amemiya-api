from fastapi import APIRouter, Request, status
from fastapi.responses import PlainTextResponse
from src.core.config import logger

router = APIRouter(prefix="/mqtt", tags=["MQTT-Auth"])


@router.post("/auth")
async def emqx_auth(request: Request):
    """Endpoint usado pelo EMQX `emqx_auth_http` plugin.

    Recebe um POST com JSON contendo at least `username` e `password` (o plugin envia clientid, username, password, ip).
    Neste projeto definimos o `password` como o JWT gerado pela API. Se o token for válido, retornamos 'allow' em texto,
    caso contrário retornamos 'deny' com status 401.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    username = body.get("username")
    password = body.get("password")

    logger.info(f"MQTT auth request for username={username}")

    if not password:
        return PlainTextResponse("deny", status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        # Validate token using jose (we decode here to ensure it's valid)
        from src.core.auth import decode_token

        payload = decode_token(password)

        # payload contains sub with user info; additional checks may be applied here
        logger.info(f"MQTT auth success for username={username}, payload={payload}")
        return PlainTextResponse("allow", status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.info(f"MQTT auth failed for username={username}: {e}")
        return PlainTextResponse("deny", status_code=status.HTTP_401_UNAUTHORIZED)
