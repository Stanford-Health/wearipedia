import os
import pickle

from garminconnect import Garmin

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import *
from .fenix_gen import *

class_name = "Fenix7S"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_fenix_data.pkl"


class Fenix7S(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = ["dates", "steps", "hrs", "brpms"]

    def _default_params(self):
        return {"start_date": "2022-03-01", "end_date": "2022-06-17"}

    def _get_data(self, data_type, params):
        return fetch_real_data(
            params["start_date"], params["end_date"], data_type, self.api
        )

    def _gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

        self.dates, self.steps, self.hrs, self.brpms = create_syn_data()

    def authenticate(self, auth_creds, use_cache=True):
        # use_cache=True is default because this API tends to rate-limit us a lot
        # authorize this device against API

        # Initialize Garmin api with your credentials
        self.auth_creds = auth_creds

        if use_cache and os.path.exists(CRED_CACHE_PATH):
            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
        else:
            self.api = Garmin(auth_creds["email"], auth_creds["password"])
            self.api.login()

            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))

        self._authenticated = True
