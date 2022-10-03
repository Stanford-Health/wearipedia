from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_gen import *

class_name = "Fenix7S"


class Fenix7S(BaseDevice):
    def __init__(self):
        self._authorized = False
        self.data_types_methods_map = {
            "dates": "get_dates",
            "steps": "get_steps",
            "hrs": "get_hrs",
            "brpms": "get_brpms",
        }

    def get_dates(self, params=None):
        if hasattr(self, "dates"):
            return self.dates

        start_date = "2022-03-01"  # @param {type:"string"}
        end_date = "2022-06-17"  # @param {type:"string"}

        return self.dates

    def get_steps(self, params=None):
        if hasattr(self, "steps"):
            return self.steps

        return self.steps

    def get_hrs(self, params=None):
        if hasattr(self, "hrs"):
            return self.hrs

        return self.hrs

    def get_brpms(self, params=None):
        if hasattr(self, "brpms"):
            return self.brpms

        return self.brpms

    def _get_data(self, data_type, params=None):
        if params is None:
            params = dict()

        return getattr(self, self.data_types_methods_map[data_type])(params=params)

    def gen_synthetic_data(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

        self.dates, self.steps, self.hrs, self.brpms = create_syn_data()

    def authorize(self, auth_creds):
        # authorize this device against API

        self.auth_creds = auth_creds

        # Initialize Garmin api with your credentials
        api = Garmin(auth_creds["email"], auth_creds["password"])

        api.login()

        self._authorized = True
