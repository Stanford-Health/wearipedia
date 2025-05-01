from datetime import datetime

import requests
import urllib3

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .strava_fetch import fetch_real_data
from .strava_syn_gen import create_syn_data
from .strava_syn_gen_streams import return_streams_syn


class Strava(BaseDevice):

    """This device allows you to work with data from the `Strava <https://www.strava.com/>`_ app.
    Available datatypes for this device are:

    * `distance`: a list that contains distance ran for each run recorded

    * `moving_time`: a list that contains moving time for each run recorded

    * `elapsed_time`: a list that contains elapsed time for each run recorded

    * `total_elevation_gain`: a list that contains total elevation gain for each run recorded

    * `average_speed`: a list that contains average speed for each run recorded

    * `max_speed`: a list that contains max speed for each run recorded

    * `average_heartrate`: a list that contains average heartrate for each run recorded

    * `max_heartrate`: a list that contains max heartrate for each run recorded

    * `map_summary_polyline`: a list that contains map summary polyline for each run recorded

    * `elev_high`: a list that contains elevation high for each run recorded

    * `elev_low`: a list that contains elevation low for each run recorded

    * `average_cadence`: a list that contains average cadence for each run recorded

    * `average_watts`: a list that contains average watts for each run recorded

    * `kilojoules`: a list that contains kilojoules for each run recorded

    * `heartrate`: a list that contains heartrate for each run recorded (stream data). Use id to specify the specific activity.


    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    :param id : id of the activity, defaults to '', required for stream data
    :type id: str, optional
    """

    name = "strava/strava"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):

        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }

        self._initialize_device_params(
            [
                "distance",
                "moving_time",
                "elapsed_time",
                "total_elevation_gain",
                "average_speed",
                "max_speed",
                "average_heartrate",
                "max_heartrate",
                "map_summary_polyline",
                "elev_high",
                "elev_low",
                "average_cadence",
                "average_watts",
                "kilojoules",
                "heartrate",
            ],
            params,
            {
                "seed": 0,
                "start_date": "2022-03-01",
                "end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["start_date"],
            "end_date": self.init_params["end_date"],
        }

    def _get_real(self, data_type, params):
        if "id" in params:
            return fetch_real_data(
                self, params["start_date"], params["end_date"], data_type, params["id"]
            )
        return fetch_real_data(
            self, params["start_date"], params["end_date"], data_type
        )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        stream_data = {"heartrate"}

        if data_type in stream_data:
            return data

        def date_str_to_obj(x):
            return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):

        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        default_cols = ["name", "id", "start_date"]

        # generate synthetic data frame based on start and end dates
        self.synthetic_df = create_syn_data(
            self.init_params["start_date"],
            self.init_params["end_date"],
        )

        self.distance = list(
            self.synthetic_df.get(default_cols + ["distance"]).to_dict("index").values()
        )
        self.moving_time = list(
            self.synthetic_df.get(default_cols + ["moving_time"])
            .to_dict("index")
            .values()
        )
        self.elapsed_time = list(
            self.synthetic_df.get(default_cols + ["elapsed_time"])
            .to_dict("index")
            .values()
        )
        self.total_elevation_gain = list(
            self.synthetic_df.get(default_cols + ["total_elevation_gain"])
            .to_dict("index")
            .values()
        )
        self.average_speed = list(
            self.synthetic_df.get(default_cols + ["average_speed"])
            .to_dict("index")
            .values()
        )
        self.max_speed = list(
            self.synthetic_df.get(default_cols + ["max_speed"])
            .to_dict("index")
            .values()
        )
        self.average_heartrate = list(
            self.synthetic_df.get(default_cols + ["average_heartrate"])
            .to_dict("index")
            .values()
        )
        self.max_heartrate = list(
            self.synthetic_df.get(default_cols + ["max_heartrate"])
            .to_dict("index")
            .values()
        )
        self.map_summary_polyline = list(
            self.synthetic_df.get(default_cols + ["map.summary_polyline"])
            .to_dict("index")
            .values()
        )
        self.elev_high = list(
            self.synthetic_df.get(default_cols + ["elev_high"])
            .to_dict("index")
            .values()
        )
        self.elev_low = list(
            self.synthetic_df.get(default_cols + ["elev_low"]).to_dict("index").values()
        )
        self.average_cadence = list(
            self.synthetic_df.get(default_cols + ["average_cadence"])
            .to_dict("index")
            .values()
        )
        self.average_watts = list(
            self.synthetic_df.get(default_cols + ["average_watts"])
            .to_dict("index")
            .values()
        )
        self.kilojoules = list(
            self.synthetic_df.get(default_cols + ["kilojoules"])
            .to_dict("index")
            .values()
        )
        self.heartrate = return_streams_syn("heartrate")

    def _authenticate(self, auth_creds):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # The auth_url specifies the URL to the endpoint that authenticates user credentials
        auth_url = "https://www.strava.com/oauth/token"

        # payload sends the user's credentials to the API during POST request
        payload = {
            "client_id": auth_creds["client_id"],
            "client_secret": auth_creds["client_secret"],
            "refresh_token": auth_creds["refresh_token"],
            "grant_type": "refresh_token",
            "f": "json",
        }

        print("Requesting Token...\n")
        # POST request to get the participant's ACCESS TOKEN
        res = requests.post(auth_url, data=payload, verify=False)
        # saving the participant's ACCESS TOKEN
        if "message" in res.json():
            return res.json()["message"]
        self.access_token = res.json()["access_token"]
        print(f"Access Token = {self.access_token}\n")
