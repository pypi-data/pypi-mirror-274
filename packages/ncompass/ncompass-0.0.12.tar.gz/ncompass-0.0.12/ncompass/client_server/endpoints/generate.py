import time
import asyncio
from fastapi import Request
from fastapi.responses import Response, JSONResponse
from typing import Any, Coroutine, Callable, Optional

from .endpoint import Endpoint

from ncompass.client import nCompass

class Generate(Endpoint):
    def __init__(self
                 , api_key: str
                 , custom_env_var: Optional[str] = None
                 , api_url: Optional[str] = None):
        self.client = nCompass( api_key = api_key
                              , custom_env_var = custom_env_var
                              , api_url = api_url )
        self.client.start_session()
        self.client.wait_until_model_running()

    def __del__(self):
        self.client.stop_session()

    @property
    def url(self) -> str:
        return '/generate'
    
    @property
    def handler(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return self.generate
    
    async def generate(self, request: Request) -> Response:
        req = await request.json()
        if req['stream'] == False:
            batch_size = req.pop('batch_size')
            prompt = [req.pop('prompt')] * batch_size
            try:
                start = time.perf_counter()
                response = self.client.complete_prompt(prompt, **req) 
                elapsed = time.perf_counter() - start
                return JSONResponse( { 'response': response
                                     , 'query_time_ms': elapsed*1000 }
                                   , status_code=200 )
            except Exception as e:
                return Response(status_code = 500
                                , content = str(e))
        else:
            return Response(status_code = 501
                            , content = ('nCompass client server mode does not support '
                                         'streaming yet!'))
