#### sleep gives us bad data, so need to figure this one out


import os
from pathlib import Path

import wget

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .withings_authenticate import *
from .withings_extract import *

class_name = "SleepMat"


class SleepMat(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = ["measurements"]

    def _get_data(self, data_type, params=None):
        if hasattr(self, data_type):
            return getattr(self, data_type)

        return fetch_measurements(self.access_token)

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

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

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

        self.access_token = withings_authenticate(auth_creds)
        self._authenticated = True
