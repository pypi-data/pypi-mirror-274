import sys
import ncompass.client.functional as F
from ncompass.network_utils import platform_url

def start_model(api_key):
    F.start_model(platform_url(), api_key)

def main():
    start_model(sys.argv[1])
