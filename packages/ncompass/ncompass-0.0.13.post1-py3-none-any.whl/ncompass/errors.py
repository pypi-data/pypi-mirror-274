
def error_msg(err):
    raise RuntimeError(f'{err}:\nPlease contact admin@ncompass.tech for resolution.') 

def api_key_not_set(custom_var = None):
    if custom_var is not None:
        raise RuntimeError(\
                f'Env variable {custom_var} not set to api key. Please set this and run again.')
    else:
        raise RuntimeError(\
                'Env variable NCOMPASS_API_KEY needs to be set to the api key. ' 
                'Alternatively, pass a custom variable.')

def model_not_started(api_key):
    msg = (f'Model {api_key} has not been started or is currently starting. '
           f'To start model use cli and run `nccli-start-model {api_key}`\n'
           f'Once you have started it, check status with `nccli-model-status {api_key}`\n'
            'Plese wait until `nccli-model-status` succeeds before trying to run the program again. '
            'If this still does not work, please contact admin@ncompass.tech for support')
    raise RuntimeError(msg)

def cannot_set_event_loop(in_msg):
    msg = (f'Pass event loop to client init or call nCompassOLOC().set_event_loop '
           f'in main OS thread! :: {in_msg}') 
    raise RuntimeError(msg)

