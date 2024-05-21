import json
from ncompass.errors import error_msg

def extract_delta(msg, chat_interface, stream):
    _delta = msg['choices'][0]
    if chat_interface: 
        delta = _delta['delta'] if stream else _delta['message']
        if 'content' in delta.keys(): return delta['content']
    else:              
        return _delta['text']

def stream_response_handler(chat_interface):
    async def wrapper(_response):
        async def handler(response):
            async for (_message, _) in response.content.iter_chunks():
                for message in _message.split(b"\n\n"):
                    if len(message) == 0: continue
                    
                    if message.startswith( b"data:"):
                        message = message.strip()
                        message = message[len(b"data:") :]
                        msg = message.decode()
                        try:
                            msg = json.loads(msg)
                            yield extract_delta(msg, chat_interface, stream=True)
                        except Exception as _:
                            continue
        return handler(_response)
    return wrapper

def batch_response_handler(chat_interface):
    async def handler(response):
        res = await response.json()
        return extract_delta(res, chat_interface, stream=False)
    return handler 
