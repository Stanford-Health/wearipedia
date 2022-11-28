import http
import json

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .pro_cgm_fetch import *
from .pro_cgm_gen import *

class_name = "DexcomProCGM"


class DexcomProCGM(BaseDevice):
    def __init__(self, params):
        self._initialize_device_params(
            ["dataframe"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-02-16",
                "synthetic_end_date": "2022-05-15",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        # there is really only one data type for this device,
        # so we don't need to check the data_type

        return fetch_data(
            self.access_token,
            start_date=params["start_date"],
            end_date=params["end_date"],
        )

    def _filter_synthetic(self, data, data_type, params):
        # there is really only one data type for this device,
        # so we don't need to check the data_type

        start_ts = pd.Timestamp(params["start_date"])
        end_ts = pd.Timestamp(params["end_date"])

        start_idx = bin_search(np.array(self.dataframe.datetime), start_ts)
        end_idx = bin_search(np.array(self.dataframe.datetime), end_ts)

        return self.dataframe.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.dataframe = create_synth_df(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def _authenticate(self, auth_creds, use_cache=True):
        if use_cache and hasattr(self, "access_token"):
            return

        if "refresh_token" in auth_creds:
            self.refresh_token, self.access_token = refresh_access_token(
                auth_creds["refresh_token"],
                auth_creds["client_id"],
                auth_creds["client_secret"],
            )
        else:
            self.refresh_token, self.access_token = dexcom_authenticate(
                auth_creds["client_id"], auth_creds["client_secret"]
            )
