import requests
from requests.exceptions import HTTPError
import time

class LiveScoreAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://livescore-api.com/api-client"

    def get_live_scores(self):
        max_retries = 3
        backoff_factor = 2 # constant which is used for exponential backoff strategy
        retries = 0
        wait = 0
        while retries < max_retries:
            url = f"{self.base_url}/matches/live.json?&key={self.api_key}&secret={self.api_secret}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                return response.json().get("data")
            except HTTPError as e:
                if 500 <= e.response.status_code < 600: # Server error (5xx)
                    retries += 1
                    wait_time = wait * (backoff_factor ** (retries - 1))
                    print(f"Server error, retrying in {wait_time} seconds... (Retry {retries}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise e
        raise Exception(f"Maximum retries exceeded for the API request.")