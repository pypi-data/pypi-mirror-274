import sys
import ncompass.client.functional as F
from ncompass.network_utils import exec_url

def model_status(api_key):
    response = F.model_health.check_model_health(exec_url(), api_key)
    if (response.status_code == 200) or (response.status_code == 400):
        print('Model is running!')
    elif response.status_code == 404:
        print('Need to start model. If you already have, please wait')
    elif response.status_code == 504:
        print('Please contact admin@ncompass.tech, there is an internal server error')

def main():
    model_status(sys.argv[1])
