import asyncio
import argparse
from fastapi import FastAPI

from .endpoints import Health, Generate

def setup_endpoints(fastapi_args: argparse.Namespace
                    , ncompass_args: argparse.Namespace) -> FastAPI:
    app = FastAPI()
    app.root_path = fastapi_args.root_path
    register_endpoints(app, ncompass_args)
    return app

def register_endpoints(app: FastAPI
                       , ncompass_args: argparse.Namespace) -> None:
    health = Health()
    app.get(health.url)(health.handler) 

    generate = Generate(**vars(ncompass_args))
    app.post(generate.url)(generate.handler) 
    
