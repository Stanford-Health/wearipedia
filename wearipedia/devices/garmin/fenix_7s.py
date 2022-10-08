import json
import pickle

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import *
from .fenix_gen import *

class_name = "Fenix7S"

CRED_CACHE_PATH = "/tmp/wearipedia_fenix_data.json"
CRED_CACHE_PATH = "/tmp/wearipedia_fenix_data.pkl"


class Fenix7S(BaseDevice):
    def __init__(self):
        self._authorized = False
        self.valid_data_types = ["dates", "steps", "hrs", "brpms"]

    def _get_data(self, data_type, params=None):
        if params is None:
            params = {"start_date": "2022-03-01", "end_date": "2022-06-17"}

        if hasattr(self, data_type):
            return getattr(self, data_type)

        return fetch_real_data(
            params["start_date"], params["end_date"], data_type, self.api
        )

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

        self.dates, self.steps, self.hrs, self.brpms = create_syn_data()

    def authorize(self, auth_creds, use_cache=False):
        # authorize this device against API

        # Initialize Garmin api with your credentials
        self.auth_creds = auth_creds

        if use_cache:
            # self.api.modern_rest_client.clear_cookies()
            # self.api.sso_rest_client.clear_cookies()
            # cache_dict = json.load(open(CRED_CACHE_PATH, 'r'))

            # self.api.display_name = cache_dict['display_name']
            # self.api.unit_system = cache_dict['unit_system']
            # self.api.full_name = cache_dict['full_name']
            # self.api.session_data = cache_dict['session_data']

            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))

        else:
            self.api = Garmin(auth_creds["email"], auth_creds["password"])
            # todo: cache the login to some semi-permanent location in the filesystem, e.g. /tmp/wearipedia-cache,
            # so that we don't get rate-limited in our logins by Garmin
            self.api.login()

            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))

            # cache_dict = {'display_name': self.api.display_name,
            #    'unit_system': self.api.unit_system,
            #    'full_name': self.api.full_name,
            #    'session_data': self.api.session_data
            # }

            # with open(CRED_CACHE_PATH, 'w') as f:
            #    json.dump(cache_dict, f)

        self._authorized = True
