from datetime import datetime

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .apple_gen import create_syn_data


class HealthKit(BaseDevice):
    """This device allows you to work with data from `Apple HealthKit <https://www.apple.com/ios/health/>`_ .
    Available datatypes for this device are:

    * `dates`: a list of consecutive dates

    * `steps`: a sibling list to `dates` that contains step data for each day

    * `hrs`: a sibling list to `dates` that contains heart rate data for each day

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "apple/healthkit"

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2022-03-01",
        synthetic_end_date="2022-06-17",
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            ["dates", "steps", "hrs"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

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
        seed_everything(self.init_params["seed"])

        self.dates, self.steps, self.hrs = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
