import sys
import ncompass.client.functional as F
from ncompass.network_utils import exec_url

def help_msg():
    print('\t nccli-help :: Prints this help message.')

def start_model_msg():
    print('\t nccli-start-model <api_key> :: Starts the model for an api_key')

def start_session_msg():
    print('\t nccli-start-session <api_key> :: Starts the session for an api_key')

def stop_model_msg():
    print('\t nccli-stop-model <api_key> :: Stops the model for an api_key')

def stop_session_msg():
    print('\t nccli-stop-session <api_key> :: Stops the session for an api_key')

def model_status_msg():
    print('\t nccli-model-status <api_key> :: Return status msg for api_key')

def help():
    print('Usage instructions for the nCompass cli (nccli-):')
    help_msg()
    start_model_msg()
    start_session_msg()
    stop_model_msg()
    stop_session_msg()
    model_status_msg()

def main():
    help()
