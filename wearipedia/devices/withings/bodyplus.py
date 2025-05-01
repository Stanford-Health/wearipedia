import os
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import wget

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .withings_authenticate import refresh_access_token, withings_authenticate
from .withings_extract import fetch_measurements
from .withings_gen import create_syn_bodyplus


class BodyPlus(BaseDevice):
    """This device allows you to work with data from the `Withings Body+ <https://www.withings.com/us/en/body-plus>`_ device.
    Available datatypes for this device are:

    * `measurements`: contains all measurements made with the scale

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2021-06-01"
    :type start_date: str, optional
    """

    name = "withings/bodyplus"

    def __init__(self, seed=0, synthetic_start_date="2021-06-01"):

        params = {"seed": seed, "synthetic_start_date": synthetic_start_date}

        self._initialize_device_params(
            ["measurements"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2021-06-01",
            },
        )

    def _default_params(self):
        return {
            "start": self.init_params["synthetic_start_date"],
            "end": datetime.strftime(
                datetime.strptime(self.init_params["synthetic_start_date"], "%Y-%m-%d")
                + timedelta(days=900),
                "%Y-%m-%d",
            ),
        }

    def _get_real(self, data_type, params):
        start = datetime.strptime(params["start"], "%Y-%m-%d")
        end = datetime.strptime(params["end"], "%Y-%m-%d")

        return fetch_measurements(self.access_token, start, end)

    def _filter_synthetic(self, data, data_type, params):
        start_ts = pd.Timestamp(params["start"])
        end_ts = pd.Timestamp(params["end"])

        start_idx = bin_search(np.array(data.date), start_ts)
        end_idx = bin_search(np.array(data.date), end_ts)

        return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.measurements = create_syn_bodyplus(
            self.init_params["synthetic_start_date"]
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
