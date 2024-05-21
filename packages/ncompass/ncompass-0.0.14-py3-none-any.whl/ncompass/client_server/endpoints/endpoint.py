from typing import Any, Coroutine, Callable

class Endpoint():
    @property
    def url(self) -> str:
        raise NotImplementedError('url needs to be set for endpoint')

    @property
    def handler(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        raise NotImplementedError('handler function needs to be set for endpoint')
