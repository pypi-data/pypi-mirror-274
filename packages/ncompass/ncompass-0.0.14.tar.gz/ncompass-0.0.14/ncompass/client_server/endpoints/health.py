from fastapi.responses import Response
from typing import Any, Coroutine, Callable

from .endpoint import Endpoint

class Health(Endpoint):
    @property
    def url(self) -> str:
        return '/health'
    
    @property
    def handler(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return get_health

async def get_health() -> Response:
    return Response(status_code=200
                    , content='nCompass audioserver is healthy!')
