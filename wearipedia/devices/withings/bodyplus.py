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


class BodyPlus(BaseDevice):
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

    def _get_synthetic(self, data_type, params):
        return self.measurements

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

        self.measurements = self.measurements[
            [col for col in self.measurements.columns if "Unnamed: 0" not in col]
        ]

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

        self.access_token = withings_authenticate(auth_creds)
        self._authenticated = True
