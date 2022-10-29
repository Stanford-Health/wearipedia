import os
from pathlib import Path

import wget

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .withings_authenticate import *
from .withings_extract import *
from .withings_gen import *

CSV_URL = "https://gist.githubusercontent.com/stanford-health-wearables/3e5bdd4dfc06a4290038fabf34732ca3/raw/c99a50c1d943903c867364dc6c9a11d83fb4e42a/random_data.csv"
CSV_LOCAL_PATH = "/tmp/wearipedia-cache/withings/bodyplus/random_data.csv"

os.makedirs(Path(CSV_LOCAL_PATH).parent, exist_ok=True)

class_name = "BodyPlus"


class BodyPlus(BaseDevice):
    def __init__(self, params):

        self._initialize_device_params(
            ["measurements"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2021-06-01",
                "synthetic_end_date": "2022-05-30",
            },
        )

    def _default_params(self):
        return {
            "start": self.init_params["synthetic_start_date"],
            "end": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_measurements(self.access_token)

    def _filter_synthetic(self, data, data_type, params):
        start_ts = pd.Timestamp(params["start"])
        end_ts = pd.Timestamp(params["end"])

        start_idx = bin_search(np.array(data.date), start_ts)
        end_idx = bin_search(np.array(data.date), end_ts)

        return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.measurements = create_syn_bodyplus()

    def _authenticate(self, auth_creds):
        self.access_token = withings_authenticate(auth_creds)
