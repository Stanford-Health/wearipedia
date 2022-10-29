from datetime import datetime

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .whoop_gen import *
from .whoop_user import *

class_name = "Whoop4"


def bin_search(data, start, end, target):
    if start >= end:
        return start

    mid = (start + end) // 2
    if data[mid] == target:
        return mid
    elif data[mid] < target:
        return bin_search(data, mid + 1, end, target)
    else:
        return bin_search(data, start, mid - 1, target)


class Whoop4(BaseDevice):
    def __init__(self, params):

        self.data_types_methods_map = {
            "cycles": "get_cycles_df",
            "health_metrics": "get_health_metrics_df",
            "sleeps": "get_sleeps_df",
            "hr": "get_heart_rate_df",
        }

        self._initialize_device_params(
            list(self.data_types_methods_map.keys()),
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        start_str = "2000-01-01"
        end_str = "2100-02-03"
        # get cycle data from start to end
        params = {
            "start": start_str + "T00:00:00.000Z",
            "end": end_str + "T00:00:00.000Z",
        }

        return params

    def _get_real(self, data_type, params):
        api_func = getattr(self.user, self.data_types_methods_map[data_type])
        return api_func(params=params)

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        if data_type != "hr":
            # synthetic data is generated day-by-day, so we can just
            # index into it based on the start and end dates

            date_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")
            datetime_str_to_obj = lambda x: datetime.strptime(
                x, "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            # get the indices by subtracting against the start of the synthetic data
            synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

            start_idx = (datetime_str_to_obj(params["start"]) - synthetic_start).days
            end_idx = (datetime_str_to_obj(params["end"]) - synthetic_start).days

            return data.iloc[start_idx:end_idx]
        else:
            # hr data is generated in 7 second intervals, so we need to
            # do a binary search to find the start and end indices
            # and then return the data between those indices

            start_ts = pd.Timestamp(params["start"])
            end_ts = pd.Timestamp(params["end"])

            start_idx = bin_search(np.array(data.timestamp), 0, len(data) - 1, start_ts)
            end_idx = bin_search(np.array(data.timestamp), 0, len(data) - 1, end_ts)

            return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.cycles = create_fake_cycles_df()

        self.health_metrics = create_fake_metrics_df()

        self.sleeps = create_fake_sleeps_df()

        self.hr = create_fake_hr_df(self.sleeps)

    def _authenticate(self, auth_creds):
        # authenticate this device against API

        self.user = WhoopUser(auth_creds["email"], auth_creds["password"])
