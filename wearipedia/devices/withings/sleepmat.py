#### sleep gives us bad data, so need to figure this one out


import os
from pathlib import Path

import wget

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .withings_authenticate import refresh_access_token, withings_authenticate
from .withings_extract import (
    fetch_all_sleep_summaries,
    fetch_all_sleeps,
    fetch_measurements,
)


class SleepMat(BaseDevice):

    name = "withings/sleepmat"

    def __init__(self, seed=0):

        params = {
            "seed": seed,
        }

        self._initialize_device_params(
            ["sleep", "sleep_summary"],
            params,
            {"seed": 0},
        )

    def _default_params(self):
        return dict()

    def _get_real(self, data_type, params):
        if data_type == "sleep":
            return fetch_all_sleeps(self.access_token, params["start"], params["end"])
        elif data_type == "sleep_summary":
            return fetch_all_sleep_summaries(
                self.access_token, params["start"], params["end"]
            )
        return fetch_measurements(self.access_token, params["start"], params["end"])

    def _filter_synthetic(self, data, data_type, params):
        return []

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.sleep = []
        self.sleep_summary = []

        # load in the CSV that we've pre-generated
        # wget.download(CSV_URL, out=CSV_LOCAL_PATH)

        # self.measurements = pd.read_csv(CSV_LOCAL_PATH)
        # fix dates, convert to datetime obj from string
        # self.measurements["date"] = self.measurements.date.apply(
        #    lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        # )

        # self.measurements = self.measurements[
        #    [col for col in self.measurements.columns if "Unnamed: 0" not in col]
        # ]

    def _authenticate(self, auth_creds):
        if "refresh_token" in auth_creds:
            self.refresh_token, self.access_token = refresh_access_token(
                auth_creds["refresh_token"],
                auth_creds["client_id"],
                auth_creds["customer_secret"],
            )
        else:
            self.refresh_token, self.access_token = withings_authenticate(
                auth_creds["client_id"], auth_creds["customer_secret"]
            )
