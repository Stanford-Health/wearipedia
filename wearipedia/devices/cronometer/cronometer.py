from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .cronometer_fetch import fetch_real_data
from .cronometer_synthetic import create_syn_data

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_cronometer_data.pkl"


class Cronometer(BaseDevice):

    """This device allows you to work with data from the `Cronometer <https://cronometer.com/>`_ app.
    Available datatypes for this device are:

    * `dailySummary`: a list that contains daily summary data for each day

    * `servings`: a list that contains servings data for each day

    * `exercises`: a list that contains exercises data for each day

    * `biometrics`: a list that contains biometrics data for each day

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "cronometer/cronometer"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }
        self._initialize_device_params(
            ["dailySummary", "servings", "exercises", "biometrics"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-09-17",
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

        def date_str_to_obj(x):
            return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        if data_type in ["exercises", "biometrics"]:
            return data[start_idx * 2 : end_idx * 2]
        else:
            return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        (
            self.dailySummary,
            self.servings,
            self.exercises,
            self.biometrics,
        ) = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def _authenticate(self, auth_creds):

        # creating a requests session to store cookies
        s = requests.Session()

        # saving the session to the class
        self.session = s

        # getting the login page to extract the csrf token
        res = s.get("https://cronometer.com/login/")

        # parsing the html
        soup = BeautifulSoup(res.text, "html.parser")

        # extracting the csrf token
        anticsrf = soup.find("input", {"name": "anticsrf"}).get("value")

        if len(anticsrf) == 0:
            raise Exception("Could not find csrf token, authentication failed")

        # saving the csrf token to the class
        self.anticsrf = anticsrf

        # creating the payload
        data = {
            "anticsrf": anticsrf,
            "username": auth_creds["username"],
            "password": auth_creds["password"],
        }

        # creating the header for the post request
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # creating the url for the post request
        login_url = "https://cronometer.com/login"

        # sending the post request
        client = s.post(login_url, data=data, headers=headers)

        if client.status_code != 200:
            raise Exception("Authentication failed")

        print("Authentication successful")

        # saving the session to the class after authentication
        self.session = s
