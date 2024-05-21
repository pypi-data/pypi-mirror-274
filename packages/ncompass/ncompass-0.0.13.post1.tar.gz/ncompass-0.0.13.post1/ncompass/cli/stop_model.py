import sys
import ncompass.client.functional as F
from ncompass.network_utils import platform_url

def stop_model(api_key):
    F.stop_model(platform_url(), api_key)

def main():
    stop_model(sys.argv[1])
