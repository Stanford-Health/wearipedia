import http
import json

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .pro_cgm_fetch import dexcom_authenticate, fetch_data, refresh_access_token
from .pro_cgm_gen import create_synth


class DexcomProCGM(BaseDevice):
    """This device allows you to work with data from the `Dexcom Pro CGM <https://provider.dexcom.com/products/dexcom-g6-pro>`_ device.
    Available datatypes for this device are:

    * `data`: contains all data in one dictionary

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    """

    name = "dexcom/pro_cgm"

    def __init__(
        self, seed=0, synthetic_start_date="2022-02-16", synthetic_end_date="2022-05-15"
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            ["data"],
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

        timestamps = [pd.Timestamp(x["systemTime"]) for x in self.data["egvs"]]

        start_idx = bin_search(timestamps, start_ts)
        end_idx = bin_search(timestamps, end_ts)

        return {
            "unit": "mg/dL",
            "rateUnit": "mg/dL/min",
            "egvs": self.data["egvs"][start_idx:end_idx],
        }

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.data = create_synth(
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
