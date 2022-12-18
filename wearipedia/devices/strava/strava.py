import urllib3
from datetime import datetime
import requests

from ...devices.device import BaseDevice
from ...utils import seed_everything

from .strava_fetch import *
from .strava_syn_gen import *


class_name = "Strava"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/strava.pkl"


class Strava(BaseDevice):
    def __init__(self, params):

        # use_cache just means that we'll use the cached credentials
        # as opposed to re-authenticating every time (the API tends to
        # rate-limit a lot, see this GitHub issue:
        # https://github.com/cyberjunky/python-garminconnect/issues/85

        self._initialize_device_params(
            ['distance', 'moving_time', 'elapsed_time',
             'total_elevation_gain', 'average_speed',
             'max_speed', 'average_heartrate', 'max_heartrate', 'map_summary_polyline',
             'elev_high', 'elev_low', 'average_cadence',
             'average_watts', 'kilojoules'],
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
            self, params["start_date"], params["end_date"], data_type
        )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        def date_str_to_obj(x): return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(
            self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(
            params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):

        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        default_cols = ['name', 'id', 'start_date']

        # generate synthetic data frame based on start and end dates
        self.synthetic_df = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

        self.distance = list(self.synthetic_df.get(
            default_cols+["distance"]).to_dict('index').values())
        self.moving_time = list(self.synthetic_df.get(
            default_cols+["moving_time"]).to_dict('index').values())
        self.elapsed_time = list(self.synthetic_df.get(
            default_cols+["elapsed_time"]).to_dict('index').values())
        self.total_elevation_gain = list(self.synthetic_df.get(
            default_cols+["total_elevation_gain"]).to_dict('index').values())
        self.average_speed = list(self.synthetic_df.get(
            default_cols+["average_speed"]).to_dict('index').values())
        self.max_speed = list(self.synthetic_df.get(
            default_cols+["max_speed"]).to_dict('index').values())
        self.average_heartrate = list(self.synthetic_df.get(
            default_cols+["average_heartrate"]).to_dict('index').values())
        self.max_heartrate = list(self.synthetic_df.get(
            default_cols+["max_heartrate"]).to_dict('index').values())
        self.map_summary_polyline = list(self.synthetic_df.get(
            default_cols+["map.summary_polyline"]).to_dict('index').values())
        self.elev_high = list(self.synthetic_df.get(
            default_cols+["elev_high"]).to_dict('index').values())
        self.elev_low = list(self.synthetic_df.get(
            default_cols+["elev_low"]).to_dict('index').values())
        self.average_cadence = list(self.synthetic_df.get(
            default_cols+["average_cadence"]).to_dict('index').values())
        self.average_watts = list(self.synthetic_df.get(
            default_cols+["average_watts"]).to_dict('index').values())
        self.kilojoules = list(self.synthetic_df.get(
            default_cols+["kilojoules"]).to_dict('index').values())

    def _authenticate(self, auth_creds):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # The auth_url specifies the URL to the endpoint that authenticates user credentials
        auth_url = "https://www.strava.com/oauth/token"

        # payload sends the user's credentials to the API during POST request
        payload = {
            'client_id': auth_creds['client_id'],
            'client_secret': auth_creds['client_secret'],
            'refresh_token': auth_creds['refresh_token'],
            'grant_type': "refresh_token",
            'f': 'json'
        }

        print("Requesting Token...\n")
        # POST request to get the participant's ACCESS TOKEN
        res = requests.post(auth_url, data=payload, verify=False)
        # saving the participant's ACCESS TOKEN
        if 'message' in res.json():
            return res.json()['message']
        self.access_token = res.json()['access_token']
        print("Access Token = {}\n".format(self.access_token))
        print('Authenticated!\n')

        # figure out how to cache this, considering I am not using an API
        # pickle.dump(self, open(CRED_CACHE_PATH, "wb"))
