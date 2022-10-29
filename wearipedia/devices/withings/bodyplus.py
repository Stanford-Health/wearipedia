import os
from pathlib import Path

import wget

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .withings_authenticate import *
from .withings_extract import *

CSV_URL = "https://gist.githubusercontent.com/stanford-health-wearables/3e5bdd4dfc06a4290038fabf34732ca3/raw/c99a50c1d943903c867364dc6c9a11d83fb4e42a/random_data.csv"
CSV_LOCAL_PATH = "/tmp/wearipedia-cache/withings/bodyplus/random_data.csv"

os.makedirs(Path(CSV_LOCAL_PATH).parent, exist_ok=True)

class_name = "BodyPlus"


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


class BodyPlus(BaseDevice):
    def __init__(self, params):

        self._initialize_device_params(
            ["measurements"],
            params,
            {"seed": 0, "synthetic_start": "2021-06-01", "synthetic_end": "2022-05-30"},
        )

    def _default_params(self):
        return {
            "start": self.init_params["synthetic_start"],
            "end": self.init_params["synthetic_end"],
        }

    def _get_real(self, data_type, params):
        return fetch_measurements(self.access_token)

    def _filter_synthetic(self, data, data_type, params):
        start_ts = pd.Timestamp(params["start"])
        end_ts = pd.Timestamp(params["end"])

        start_idx = bin_search(np.array(data.date), 0, len(data) - 1, start_ts)
        end_idx = bin_search(np.array(data.date), 0, len(data) - 1, end_ts)

        return data.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # load in the CSV that we've pre-generated
        wget.download(CSV_URL, out=CSV_LOCAL_PATH)

        self.measurements = pd.read_csv(CSV_LOCAL_PATH)
        # fix dates, convert to datetime obj from string
        self.measurements["date"] = self.measurements.date.apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        )

        # filter out the unnamed column that pandas adds in for some reason
        self.measurements = self.measurements[
            [col for col in self.measurements.columns if "Unnamed: 0" not in col]
        ]

    def _authenticate(self, auth_creds):
        # authenticate this device against API

        self.access_token = withings_authenticate(auth_creds)
