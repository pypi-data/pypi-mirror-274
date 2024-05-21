import copy
import asyncio
import uvicorn
import argparse
import nest_asyncio 

from ncompass.client_server import app as client_app

def main():
    # Required so we can use functions like loop.run_until_complete() inside a ASGII server like
    # uvicorn which has an existing running event loop. Alternative to this would be to create an
    # entirely async version of the client as you can run 'await coro_1()' instead of
    # loop.run_until_complete(coro_1()) inside an ASGII server.
    nest_asyncio.apply()
    
    args_parser = argparse.ArgumentParser(prog='nCompass Client Server')
    
    # FastAPI Arguments
    fastapi_parser = args_parser.add_argument_group('fastapi')
    fastapi_parser.add_argument('--root_path', type=str, default=None)
    
    # Uvicorn Arguments
    uvicorn_parser = args_parser.add_argument_group('uvicorn')
    uvicorn_parser.add_argument('--host', type=str, default='127.0.0.1')
    uvicorn_parser.add_argument('--port', type=int, default=8000)
    uvicorn_parser.add_argument('--ssl_keyfile', type=str, default=None)
    uvicorn_parser.add_argument('--ssl_certfile', type=str, default=None)
    uvicorn_parser.add_argument('--timeout_keep_alive', type=int, default=30)
    uvicorn_parser.add_argument('--limit_concurrency', type=int, default=1000)
    
    # nCompass Arguments
    ncompass_parser = args_parser.add_argument_group('ncompass')
    ncompass_parser.add_argument('--api_key'
                                , type=str
                                , required=True
                                , help=f'Provide api_key for model')
    ncompass_parser.add_argument('--api_url'
                                , type=str
                                , help=f'Provide url of device running the model')
    ncompass_parser.add_argument('--custom_env_var'
                                , type=str
                                , help=f'Env var where api_key is stored. Alternative to --api_key')
    
    args = args_parser.parse_args()

    arg_groups = {}
    for group in args_parser._action_groups:
        group_dict = {a.dest: getattr(args, a.dest, None) for a in group._group_actions}
        arg_groups[group.title] = argparse.Namespace(**group_dict)
    
    app = client_app.setup_endpoints(arg_groups['fastapi'], arg_groups['ncompass'])
    uvicorn.run(app, **vars(arg_groups['uvicorn']))    
