from datetime import datetime
import requests

from ..device import BaseDevice
from ...utils import seed_everything

from .googlefitness_fetch import *

class_name = "GoogleFitness"

class GoogleFitness(BaseDevice):
    def __init__(self, params):

        # use_cache just means that we'll use the cached credentials
        # as opposed to re-authenticating every time (the API tends to
        # rate-limit a lot, see this GitHub issue:
        #
        self._initialize_device_params(
            ['steps','heart_rate', 'sleep', 'heart_minutes','blood_pressure', 'blood_glucose', 'body_temperature', 'calories_expended', 'activity', 'height', 'move_minutes', 'oxygen_saturation', 'mensuration', 'speed', 'weight','distance'],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "time_bucket": "86400000",
                "use_cache": True,
            },
        )
    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
            "time_bucket": self.init_params["time_bucket"],
        }

    def _get_real(self, data_type, params):
        if 'time_bucket' not in params:
            return fetch_real_data(self,params["start_date"], params["end_date"], data_type)
        return fetch_real_data(
            self,params["start_date"], params["end_date"], data_type, params['time_bucket']
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
       
        if 'access_token' not in auth_creds:
            raise ValueError('access_token not found in credentials')

        # The auth_url specifies the URL to the endpoint that authenticates user credentials
        auth_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources"

        # The acces token that enables us to access the user's data using google's API
        g_access_token = auth_creds['access_token']

        #headers sends the user's credentials to the API during POST request
        headers = {
        "Authorization": "Bearer {}".format(g_access_token),
        "Content-Type": "application/json;encoding=utf-8"
        }

        #POST request to get the participant's ACCESS TOKEN
        res = requests.get(auth_url, headers=headers)

        # saving the participant's ACCESS TOKEN
        if res.status_code == 200:
            self.access_token = auth_creds['access_token']
            print('Authenticated!\n')
        else:
            print('Authentication failed!\n')
            print(res.text)

        # figure out how to cache this, considering I am not using an API
        # pickle.dump(self, open(CRED_CACHE_PATH, "wb"))

    
