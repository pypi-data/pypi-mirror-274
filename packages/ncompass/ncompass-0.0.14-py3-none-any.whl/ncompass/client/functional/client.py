import aiohttp
from datetime import datetime, timedelta

from .transcribe import run_transcription
from .model_health import check_model_health
from ncompass.errors import model_not_started
from ncompass.network_utils import get, post_json
from ncompass.async_utils import run_in_event_loop
from .run_prompt import run_completion, run_chat_completion, run_external_api

def start_stop_handler(response):
    if (response.status_code == 200) or (response.status_code == 209): 
        return True
    elif (response.status_code == 400): 
        raise RuntimeError('Internal server error, contact admin@ncompass.tech')
    else: 
        raise RuntimeError(response.text)

async def close_session(session):
    return await session.close()

async def create_session():
    return aiohttp.ClientSession()

def warmup_prompt(session, url, api_key, event_loop):
    wait_until_model_running(url, api_key, timeout=2)
    for _ in complete_prompt(session
                             , url
                             , api_key
                             , prompt=''
                             , max_tokens=1
                             , temperature=0.1
                             , top_p=0.9
                             , stream=True
                             , event_loop=event_loop):
        pass

def start_model(url, api_key):
    try:
        response = post_json(f'{url}/start_model'
                              , {'miid': api_key}
                              , {'authorization': api_key})
        if response.status_code == 200:
            print(response.json()['msg'])
        else:
            print(f"Please contact admin@ncompass.tech with error {response.json()['msg']}")
    except Exception as e:
        print(f"Please contact admin@ncompass.tech with error - {str(e)}")

def stop_model(url, api_key):
    try:
        response = post_json(f'{url}/stop_model'
                              , {'miid': api_key}
                              , {'authorization': api_key})
        if response.status_code == 200:
            print(response.json()['msg'])
        else:
            print(f"Please contact admin@ncompass.tech with error - {response.json()['msg']}")
    except Exception as e:
        print(f"Please contact admin@ncompass.tech with error - {str(e)}")

def start_session(url, api_key, transcription, event_loop=None, nc_provider=True):
    session = run_in_event_loop(create_session(), event_loop)
    if nc_provider:
        try:
            start_stop_handler(get(f'{url}/start_session', {'Authorization': api_key}))
            if not transcription: warmup_prompt(session, url, api_key, event_loop)
        except Exception as e:
            run_in_event_loop(close_session(session), event_loop)
            raise e
    return session

def stop_session(url, api_key, session, event_loop=None, nc_provider=True):
    if session is not None: run_in_event_loop(close_session(session), event_loop)
    if not nc_provider : return True
    else:                return start_stop_handler(get(f'{url}/stop_session'
                                                       , {'Authorization': api_key}))

def model_is_running(url, api_key):
    try: # this try-catch looks for network connectivity issues with running check_model_health
        response = check_model_health(url, api_key)
    except Exception :
        return False
    if (response.status_code == 404):
        # Model is not in live models dictionary
        return False
    elif (response.status_code == 400):
        # Model is in live models dictionary, but not started (this is fine, just need to start
        # session)
        return True
    elif response.status_code == 200:
        return True
    elif response.status_code == 504:
        model_not_started(api_key)
    else:
        return False

def wait_until_model_running(url, api_key, timeout=20):
    break_loop = False
    wait_until = datetime.now() + timedelta(seconds=timeout)
    while not break_loop:
        if model_is_running(url, api_key): break_loop = True
        if wait_until < datetime.now():    model_not_started(api_key)

def print_prompt(response_iterator):
    [print(elem, end='', flush=True) for elem in response_iterator]
    print()

def complete_prompt(session
                    , url
                    , api_key
                    , prompt
                    , max_tokens
                    , temperature
                    , top_p
                    , stream
                    , event_loop):
    return run_completion(session
                          , url=url
                          , miid=api_key
                          , prompt=prompt
                          , max_tokens=max_tokens
                          , temperature=temperature
                          , top_p=top_p
                          , stream=stream
                          , event_loop=event_loop)
    
def complete_chat(session
                    , url
                    , api_key
                    , messages
                    , template_type
                    , add_generation_prompt
                    , max_tokens
                    , temperature
                    , top_p
                    , stream
                    , event_loop):
    return run_chat_completion(session
                               , url=url
                               , miid=api_key
                               , messages=messages
                               , template_type=template_type
                               , add_generation_prompt=add_generation_prompt
                               , max_tokens=max_tokens
                               , temperature=temperature
                               , top_p=top_p
                               , stream=stream
                               , event_loop=event_loop)

def call_external_api(session
                      , api_provider
                      , url
                      , headers
                      , payload
                      , chat_interface
                      , event_loop):
    return run_external_api(session
                            , api_provider=api_provider
                            , url=url
                            , headers=headers
                            , payload=payload
                            , chat_interface=chat_interface
                            , event_loop=event_loop)

def transcribe(session
               , url
               , api_key
               , audio_file
               , file_format
               , stream):
    return run_transcription(session
                             , url=url
                             , miid=api_key
                             , audio_file=audio_file
                             , file_format=file_format
                             , stream=stream)
