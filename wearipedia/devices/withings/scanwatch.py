import time

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .withings_authenticate import refresh_access_token, withings_authenticate
from .withings_extract import fetch_all_heart_rate, fetch_all_sleeps
from .withings_gen import create_syn_hr, create_synthetic_sleeps_df


class ScanWatch(BaseDevice):
    """This device allows you to work with data from the `Withings ScanWatch <https://www.withings.com/us/en/scanwatch>`_ device.
    Available datatypes for this device are:

    * `heart_rates`: heart rate data

    * `sleeps`: sleep data

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type end_date: str, optional
    """

    name = "withings/scanwatch"

    def __init__(
        self, seed=0, synthetic_start_date="2022-03-01", synthetic_end_date="2022-06-17"
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            ["heart_rates", "sleeps"],
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
        if data_type == "heart_rates":
            return fetch_all_heart_rate(
                self.access_token, params["start"], params["end"]
            )
        elif data_type == "sleeps":
            return fetch_all_sleeps(self.access_token, params["start"], params["end"])

    def _filter_synthetic(self, data, data_type, params):

        if data_type == "sleeps":
            key = "date"
            target_start = params["start"]
            target_end = params["end"]
        elif data_type == "heart_rates":
            key = "datetime"
            target_start = pd.Timestamp(params["start"])
            target_end = pd.Timestamp(params["end"])

        start_idx = bin_search(np.array(data[key]), target_start)
        end_idx = bin_search(np.array(data[key]), target_end)

        return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.sleeps = create_synthetic_sleeps_df(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

        self.heart_rates = create_syn_hr(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
            self.sleeps,
        )

    def _authenticate(self, auth_creds):
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
            self.refresh_token, self.access_token = withings_authenticate(
                auth_creds["client_id"], auth_creds["client_secret"]
            )
