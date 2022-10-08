import time

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .withings_authenticate import *
from .withings_extract import *

class_name = "BodyPlus"


class BodyPlus(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = ["heart_rates", "sleeps"]

    def _get_data(self, data_type, params=None):
        if params is None:
            params = {"start": "2022-03-01", "end": "2022-06-17"}

        if hasattr(self, data_type):
            return getattr(self, data_type)

        if data_type == "heart_rates":
            return fetch_all_heart_rate(
                self.access_token, params["start"], params["end"]
            )
        elif data_type == "sleeps":
            return fetch_all_sleeps(self.access_token, params["start"], params["end"])

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

        self.access_token = withings_authenticate(auth_creds)
        self._authenticated = True
