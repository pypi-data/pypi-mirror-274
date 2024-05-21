import json
from ncompass.errors import error_msg
from ncompass.network_utils import async_streaming_post_data
from ncompass.async_utils import run_in_event_loop, get_sync_generator_from_async

async def transcription_generator(response):
    async for chunk, _ in response.content.iter_chunks():
        try:
            split_chunk = chunk.split(b'\0')
            decoded_chunk = split_chunk[0].decode('utf-8')
            try:
                yield decoded_chunk 
            except Exception as e:
                try:                   error = json.loads(decoded_chunk)['error']
                except Exception as e: error = decoded_chunk
                print(f'Call failed with error: {error}')
                yield ''
        except Exception as e:
            error_msg(str(e))

async def stream_response_handler(response):
    if response.status == 200:
       return transcription_generator(response)
    else:
        res = await response.json()
        error_msg(res['error'])

async def response_handler(response):
    res = await response.json(content_type=None)
    if response.status == 200:
        return res
    elif response.status == 500:
        error_msg(f"Execution server exception: {res['error']}")
    elif response.status == 520:
        error_msg(f"Accelerator server exception: {res['error']}")
    else:
        error_msg(f"Unexpected status code {response.status}: {res}")

def run_transcription(session
                      , url
                      , miid
                      , audio_file
                      , file_format
                      , event_loop=None
                      , stream=False):
    _url = f'{url}/stream_transcription' if stream else f'{url}/batch_transcription'
    headers = {'Content-Type': f"audio/{file_format}", 'Authorization': miid} 
    with open(audio_file, 'rb') as f:
        if stream:
            result = run_in_event_loop(async_streaming_post_data(session
                                                                 , _url
                                                                 , f
                                                                 , headers
                                                                 , stream_response_handler)
                                       , event_loop)
            return get_sync_generator_from_async(result, event_loop)
        else:
            return run_in_event_loop(async_streaming_post_data(session
                                                               , _url
                                                               , f
                                                               , headers
                                                               , response_handler), event_loop)
