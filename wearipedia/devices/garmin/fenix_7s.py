import os
import pickle
from datetime import datetime

from garminconnect import Garmin

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import *
from .fenix_gen import *

class_name = "Fenix7S"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_fenix_data.pkl"


class Fenix7S(BaseDevice):
    def __init__(self, params):

        # use_cache just means that we'll use the cached credentials
        # as opposed to re-authenticating every time (the API tends to
        # rate-limit a lot, see this GitHub issue:
        # https://github.com/cyberjunky/python-garminconnect/issues/85

        self._initialize_device_params(
            ["dates", "steps", "hrs", "brpms"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "use_cache": True,
            },
        )

    def _default_params(self):
        return {"start_date": "2022-03-01", "end_date": "2022-06-17"}

    def _get_real(self, data_type, params):
        return fetch_real_data(
            params["start_date"], params["end_date"], data_type, self.api
        )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        date_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.dates, self.steps, self.hrs, self.brpms = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def authenticate(self, auth_creds):

        self.auth_creds = auth_creds

        # check if we have cached credentials
        if self.init_params["use_cache"] and os.path.exists(CRED_CACHE_PATH):
            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
        else:
            self.api = Garmin(auth_creds["email"], auth_creds["password"])
            self.api.login()

            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))

        self._authenticated = True
