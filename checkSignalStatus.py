import requests
from psutil import boot_time
from time import time
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logFile = 'checkSignalStatus.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=False)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

log = logging.getLogger('root')
log.setLevel(logging.INFO)
log.addHandler(my_handler)

# settings of a sort
TIMEOUT = 30
MAX_ENTRIES = 10
GROUND_STATION = 3086
MAX_ALLOWED_TIME_SINCE_REBOOT_S = 60 * 60 * 24 # 1 day in seconds
ENABLE_AUTO_REBOOT = True

NETWORK_BASE_URL = "https://network.satnogs.org"

# provided by SatNOGS 
class APIRequestError(IOError):
    """
    There was an error fetching the requested resource 
    """

# provided by SatNOGS
def get_paginated_endpoint(url, 
                           max_entries=None, 
                           token=None, max_retries=0, 
                           filter_output_callback=None, 
                           stop_criterion_callback=None):
    print("starting")
    try:
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=max_retries))

        if token:
            headers = {"Authorization": f"Token {token}"}
        else:
            headers = None
        
        data = []

        response = session.get(url=url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        new_data = response.json()
        if filter_output_callback:
            data.extend(filter_output_callback(new_data))
        else:
            data.extend(new_data)
        
        if(stop_criterion_callback and stop_criterion_callback(new_data)):
            return data
        
        while 'next' in response.links and (not max_entries or len(data) < max_entries):
            print("next")
            next_page_url = response.links['next']['url']

            response = session.get(url=next_page_url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()

            new_data = response.json()
            if(filter_output_callback):
                data.extend(filter_output_callback(new_data))
            else:
                data.extend(new_data)
            if stop_criterion_callback and stop_criterion_callback(new_data):
                break
    except requests.HTTPError as exception:
        raise APIRequestError from exception
    except requests.exceptions.ReadTimeout as exception:
        raise APIRequestError from exception
    
    return data

def notifyOwner():
    pass

# https://network.satnogs.org/api/observations/?ground_station=3086 
def filter(data):
    filtered_data = []
    for d in data:
        if(d["status"] != "future"):
            filtered_data.append(d)
    return filtered_data

# get the last page of observations, typically around 20, then is stopping when limited by max_entries 
observations = get_paginated_endpoint(
    f"{NETWORK_BASE_URL}/api/observations/?ground_station={GROUND_STATION}",
    max_entries=MAX_ENTRIES,
    filter_output_callback=filter
)

# count failed observations
count = 0
for obs in observations:
    if(obs["status"] == "failed"):
        count += 1

if ENABLE_AUTO_REBOOT:
    # react only if more than half of the observations failed 
    if (count > len(observations) / 2) and (time() - boot_time() < MAX_ALLOWED_TIME_SINCE_REBOOT_S):
        log.info(f"{count}/{len(observations)} observations failed, triggered reboot at {datetime.now()}")
        os.system("sudo reboot")
    elif (count > len(observations) / 2) and (time() - boot_time() >= MAX_ALLOWED_TIME_SINCE_REBOOT_S):
        notifyOwner()
else:
    if (count > len(observations) / 2):
        notifyOwner()