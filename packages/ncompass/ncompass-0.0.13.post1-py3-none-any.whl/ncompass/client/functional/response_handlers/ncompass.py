import json
from ncompass.errors import error_msg

async def response_generator(response):
    response_len = 0
    async for chunk, _ in response.content.iter_chunks():
        try:
            split_chunk = chunk.split(b'\0')
            decoded_chunk = split_chunk[0].decode('utf-8')
            try:
                data = json.loads(decoded_chunk)
                res = data['text'][0] 
                new_data = res[response_len:]
                response_len = len(res)
                yield new_data
            except Exception as e:
                yield ''
        except Exception as e:
            error_msg(str(e))

async def stream_response_handler(response):
    if response.status == 200:
       return response_generator(response)
    else:
        res = await response.json()
        error_msg(res['error'])

async def batch_response_handler(response):
    res = await response.json(content_type=None)
    if response.status == 200:
        return res['text']
    elif response.status == 499:
        error_msg("Client connection was lost on server: {res['error']}")
    elif response.status == 400:
        error_msg(f"Server failed to generate response: {res['error']}")
    else:
        error_msg(res['error'])
