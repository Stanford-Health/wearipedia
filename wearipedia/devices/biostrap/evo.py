import os
import pickle
from datetime import datetime

import requests

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .evo_fetch import *
from .evo_gen import *

class_name = "EVO"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_evo_data.pkl"


class EVO(BaseDevice):
    BASE_URL = "https://api-beta.biostrap.com"
    ACCESS_TOKEN = os.getenv("BIOSTRAP_ACCESS_TOKEN")

    def __init__(self, user_id):
        self.headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
        }
        self.user_id = user_id

    def fetch_real_data(self, start_date, end_date):
        activities = self.fetch_activities()
        biometrics = self.fetch_biometrics()
        calories = self.fetch_calories(start_date, end_date)

        return activities, biometrics, calories

    def fetch_activities(self):
        url = f"{self.BASE_URL}/v1/activities"
        params = {"user_id": self.user_id, "last-timestamp": 0, "limit": 50}
        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def fetch_biometrics(self):
        url = f"{self.BASE_URL}/v1/biometrics"
        params = {"user_id": self.user_id, "last-timestamp": 0, "limit": 50}
        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def fetch_calories(self, start_date, end_date):
        url = f"{self.BASE_URL}/v1/calorie/details"
        params = {
            "user_id": self.user_id,
            "user_timezone_offset_in_mins": -420,  # Assuming user is in Pacific Time
            "date": end_date,  # Date in format "YYYY-MM-DD"
            "granularity": "day",  # Assuming granularity is "day"
        }
        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def fetch_syn_data(self, start_date, end_date):
        # This function will be implemented later
        pass
