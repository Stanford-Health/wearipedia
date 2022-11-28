import time

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .withings_authenticate import *
from .withings_extract import *
from .withings_gen import *

class_name = "ScanWatch"


class ScanWatch(BaseDevice):
    def __init__(self, params):
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
