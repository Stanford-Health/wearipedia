from ...utils import seed_everything
from ..device import BaseDevice
from .qualtrics_fetch import *
from .qualtrics_gen import *

class_name = "Qualtrics"

class Qualtrics(BaseDevice):
    def __init__(self, seed=0, token="M4EoyhFeA6s6YpT5BB3ETS4K1fniU1f4Y7TZddkl", data_center="stanforduniversity", survey="SV_6FDXhJO8mupUnuC"):
        params = {
            "seed": seed,
            "token": str(token),
            "data_center": str(data_center),
            "survey": str(survey),
        }

        self._initialize_device_params(
            [
                "responses",
            ],
            params,
            {
                "seed": 0,
                "token": "M4EoyhFeA6s6YpT5BB3ETS4K1fniU1f4Y7TZddkl",
                "data_center": "stanforduniversity",
                "survey": "SV_6FDXhJO8mupUnuC",
            },
        )

    def _default_params(self):
        return {
            "token": self.init_params["synthetic_token"],
            "data_center": self.init_params["synthetic_data_center"],
            "survey": self.init_params["synthetic_survey"],
        }

    def _get_real(self, params):
        return fetch_real_data(
            params["token"], params["data_center"], params["survey"]
        )

    def _filter_synthetic(self, data, params):
        return data

    def _gen_synthetic(self):
        seed_everything(self.init_params["seed"])
        (
            self.responses,
        ) = create_syn_data(
            self.init_params["synthetic_token"],
            self.init_params["synthetic_data_center"],
            self.init_params["synthetic_survey"],
        )

    def _authenticate(self):
        pass
