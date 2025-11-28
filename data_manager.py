import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint
from requests.auth import HTTPBasicAuth

env_path = Path('.') /'.env'
load_dotenv(dotenv_path=env_path)

SHETTY_ENDPOINT = "https://api.sheety.co/e04639130a115a030bb1c3e740f3b070/flightDeals/prices"
SHETTY_AUTHORIZATION = os.getenv("SHETTY_AUTHORIZATION")

headers = {
    "Authorization": SHETTY_AUTHORIZATION,
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self._user = os.getenv("SHETTY_USERNAME")
        self._password = os.getenv("SHETTY_PASSWORD")
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHETTY_ENDPOINT, auth=self._authorization)
        data = response.json()
        print(data)

        self.destination_data = data["prices"]

        pprint(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):

        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }

            response = requests.put(
                url=f"{SHETTY_ENDPOINT}/{city["id"]}",
                json=new_data,
                auth=self._authorization,
            )

            print(response.text)