import os
import pickle
from datetime import datetime

import myfitnesspal

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .myfitnesspal_fetch import fetch_real_data
from .myfitnesspal_synthetic import create_syn_data


class MyFitnessPal(BaseDevice):

    """This device allows you to work with data from the `MyFitnessPal <https://www.myfitnesspal.com/>`_ app.
    Available datatypes for this device are:

    * `goals`: a list that contains goals data for each day

    * `daily_summary`: a list that contains daily summary data for each day

    * `exercises_cardio`: a list that contains cardio exercises data for each day

    * `exercises_strength`: a list that contains strength exercises data for each day

    * `lunch`: a list that contains lunch data for each day

    * `breakfast`: a list that contains breakfast data for each day

    * `dinner`: a list that contains dinner data for each day

    * `snacks`: a list that contains snacks data for each day

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "myfitnesspal/myfitnesspal"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }
        self._initialize_device_params(
            [
                "goals",
                "daily_summary",
                "exercises_cardio",
                "exercises_strength",
                "lunch",
                "breakfast",
                "dinner",
                "snacks",
            ],
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

        def date_str_to_obj(x):
            return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        (
            self.goals,
            self.daily_summary,
            self.exercises_cardio,
            self.exercises_strength,
            self.breakfast,
            self.lunch,
            self.dinner,
            self.snacks,
        ) = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def _authenticate(self, auth_creds):

        # Using cookies stored on local machine to login to myfitnesspal
        if "cookies" in auth_creds:
            try:
                client = myfitnesspal.Client(auth_creds["cookies"])
            except myfitnesspal.exceptions.MyfitnesspalLoginError as e:
                raise Exception(
                    "Could not authenticate with MyFitnessPal using the cookies provided, retry using a local machine"
                )
        else:
            try:
                client = myfitnesspal.Client()
            except myfitnesspal.exceptions.MyfitnesspalLoginError as e:
                raise Exception(
                    "Could not authenticate with MyFitnessPal using the cookies provided by your device, retry using a local machine"
                )

        self.client = client
