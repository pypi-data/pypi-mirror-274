from ncompass.network_utils import async_streaming_post_json
from ncompass.async_utils import run_in_event_loop, get_sync_generator_from_async
from ncompass.client.functional.response_handlers import nc_response_handlers\
                                                         , openai_response_handlers

def get_response_handler_pkg(api_provider):
    if api_provider is None:          return nc_response_handlers
    elif api_provider == 'openai': return openai_response_handlers
    else:                             raise NotImplementedError(\
                                            f'Response handler for {api_provider}')

def get_response_handler(stream, api_provider=None, chat_interface=None):
    pkg = get_response_handler_pkg(api_provider) 
    if stream: return pkg.stream_response_handler if chat_interface is None \
                        else pkg.stream_response_handler(chat_interface)
    else:      return pkg.batch_response_handler if chat_interface is None \
                        else pkg.batch_response_handler(chat_interface)

def build_prompt_body_from_params(prompt
                                  , miid
                                  , max_tokens
                                  , temperature
                                  , top_p
                                  , stream):
    body = {'prompt':        prompt
            , 'miid':        miid
            , 'max_tokens':  max_tokens
            , 'temperature': temperature
            , 'top_p':       top_p
            , 'stream':      stream}
    return body

def run_completion(session
                   , url: str
                   , miid: str
                   , prompt: str
                   , max_tokens: int
                   , temperature: float
                   , top_p: float
                   , stream: bool
                   , event_loop=None):
    _url = f'{url}/run_prompt'
    headers = {'Content-Type': "application/json", 'Authorization': miid} 
    body = build_prompt_body_from_params(prompt, miid, max_tokens, temperature, top_p, stream) 
    res = run_in_event_loop(async_streaming_post_json(session
                                                      , _url
                                                      , body
                                                      , headers
                                                      , get_response_handler(stream))
                            , event_loop)
    if stream: return get_sync_generator_from_async(res, event_loop)
    else:      return res

def build_chat_body_from_params(messages
                                , template_type
                                , add_generation_prompt
                                , miid
                                , max_tokens
                                , temperature
                                , top_p
                                , stream):
    body = {'messages':                messages
            , 'template':              template_type
            , 'add_generation_prompt': add_generation_prompt
            , 'miid':                  miid
            , 'max_tokens':            max_tokens
            , 'temperature':           temperature
            , 'top_p':                 top_p
            , 'stream':                stream}
    return body

def run_chat_completion(session
                        , url: str
                        , miid: str
                        , messages: str
                        , template_type
                        , add_generation_prompt
                        , max_tokens: int
                        , temperature: float
                        , top_p: float
                        , stream: bool
                        , event_loop=None):
    _url = f'{url}/run_prompt'
    headers = {'Content-Type': "application/json", 'Authorization': miid} 
    body = build_chat_body_from_params(messages
                                       , template_type
                                       , add_generation_prompt
                                       , miid
                                       , max_tokens
                                       , temperature
                                       , top_p
                                       , stream) 
    res = run_in_event_loop(async_streaming_post_json(session
                                                      , _url
                                                      , body
                                                      , headers
                                                      , get_response_handler(stream))
                            , event_loop)
    if stream: return get_sync_generator_from_async(res, event_loop)
    else:      return res

def run_external_api(session
                     , api_provider: str
                     , url: str
                     , headers
                     , payload
                     , chat_interface
                     , event_loop=None):
    response_handler = get_response_handler(payload['stream'], api_provider, chat_interface)
    res = run_in_event_loop(async_streaming_post_json(session
                                                      , url
                                                      , payload 
                                                      , headers
                                                      , response_handler), event_loop)
    if payload['stream']: return get_sync_generator_from_async(res, event_loop)
    else:                 return res
