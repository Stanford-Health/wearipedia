import numpy as np
import pandas as pd

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .whoop_authenticate import *
from .whoop_extract import *
from .whoop_gen import *

class_name = "Whoop4"


class Whoop4(BaseDevice):
    """This device allows you to work with data from the `WHOOP 4.0 <https://shop.whoop.com/en-us/collections/whoop4-0/?order_by=featured>`_ device.
    Available datatypes for this device are:

    * `cycles`: a DataFrame of all cycles (days)

    * `sleeps`: a DataFrame of all sleeps

    * `workouts`: a DataFrame of all workouts

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type end_date: str, optional
    """

    def __init__(
        self, seed=0, synthetic_start_date="2022-03-01", synthetic_end_date="2022-06-17"
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            ["cycles", "sleeps", "workouts"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        return {
            "start": self.init_params["synthetic_start_date"],
            "end": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        if data_type == "cycles":
            return fetch_collection(
                collection_type="Cycle",
                access_token=self.access_token,
                start_date=params["start"],
                end_date=params["end"],
            )
        elif data_type == "sleeps":
            return fetch_collection(
                collection_type="Sleep",
                access_token=self.access_token,
                start_date=params["start"],
                end_date=params["end"],
            )
        elif data_type == "workouts":
            return fetch_collection(
                collection_type="Workout",
                access_token=self.access_token,
                start_date=params["start"],
                end_date=params["end"],
            )

    def _filter_synthetic(self, data, data_type, params):

        key = "start"
        target_start = params["start"]
        target_end = params["end"]

        start_idx = bin_search(np.array(data[key]), target_start)
        end_idx = bin_search(np.array(data[key]), target_end)

        return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.cycles = create_synthetic_cycle_collection_df(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

        self.sleeps = create_synthetic_sleep_collection_df(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

        self.workouts = create_synthetic_workout_collection_df(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def _authenticate(self, auth_creds):
        # authenticate this device against API
        if "access_token" in auth_creds:
            self.access_token = auth_creds["access_token"]
            return

        if "refresh_token" in auth_creds:
            self.refresh_token, self.access_token = refresh_access_token(
                auth_creds["refresh_token"],
                auth_creds["client_id"],
                auth_creds["client_secret"],
            )
        else:
            self.refresh_token, self.access_token = whoop_authenticate(
                auth_creds["client_id"], auth_creds["client_secret"]
            )
