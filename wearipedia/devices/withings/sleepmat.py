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
    def __init__(self, params):
        self._initialize_device_params(
            ["measurements"],
            params,
            {"seed": 0},
        )

    def _default_params(self):
        return dict()

    def _get_real(self, data_type, params):
        return fetch_measurements(self.access_token)

    def _filter_synthetic(self, data, data_type, params):
        return self.measurements

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.measurements = [0, 1, 2, 3, 4, 5]

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
