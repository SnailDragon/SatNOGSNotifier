import requests

NETWORK_BASE_URL = "https://network.satnogs.org"
TIMEOUT = 30
MAX_ENTRIES = 100
GROUND_STATION = 3086

class APIRequestError(IOError):
    """
    There was an error fetching the requested resource 
    """

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
    
# https://network.satnogs.org/api/observations/?ground_station=3086 
def filter(data):
    filtered_data = []
    for d in data:
        if(d["status"] != "future"):
            filtered_data.append(d)
    return filtered_data

observations = get_paginated_endpoint(
    f"{NETWORK_BASE_URL}/api/observations/?ground_station={GROUND_STATION}",
    max_entries=MAX_ENTRIES,
    filter_output_callback=filter
)
    
count = 0
for obs in observations:
    if(obs["status"] == "failed"):
        count += 1

print(count)