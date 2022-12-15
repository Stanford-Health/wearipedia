import os
import pickle
from datetime import datetime

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .myfitnesspal_fetch import *

import myfitnesspal
import browsercookie

class_name = "MyFitnessPal"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_myfitnesspal_data.pkl"

class MyFitnessPal(BaseDevice):
    def __init__(self, params):

        # use_cache just means that we'll use the cached credentials
        # as opposed to re-authenticating every time (the API tends to
        # rate-limit a lot, see this GitHub issue:
        #

        self._initialize_device_params(
            ["goals", "daily_summary", "exercises_cardio", "exercises_strength","lunch",'breakfast','dinner','snacks'],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "use_cache": True,
            },
        )
    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(
            self,params["start_date"], params["end_date"], data_type
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

        # # and based on start and end dates
        # self.dates, self.steps, self.hrs, self.brpms = create_syn_data(
        #     self.init_params["synthetic_start_date"],
        #     self.init_params["synthetic_end_date"],
        # )

    def _authenticate(self, auth_creds):

        # Using cookies stored on local machine to login to myfitnesspal
        if 'cookies' in auth_creds:
            try:
                client = myfitnesspal.Client(auth_creds['cookies'])
            except myfitnesspal.exceptions.MyfitnesspalLoginError as e:
                print("Could not authenticate with MyFitnessPal using the cookies provided, retry using a local machine")
                return
        else:
            try:
                client = myfitnesspal.Client(browsercookie.load())
            except myfitnesspal.exceptions.MyfitnesspalLoginError as e:
                print("Could not authenticate with MyFitnessPal using the cookies provided by your device, retry using a local machine")
                return
        
        self.client = client
    
        print('Authenticated!')

        # figure out how to cache this, considering I am not using an API
        # pickle.dump(self, open(CRED_CACHE_PATH, "wb"))


    