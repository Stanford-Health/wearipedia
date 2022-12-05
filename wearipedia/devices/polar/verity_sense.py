import numpy as np

from ...devices.device import BaseDevice
from .verity_gen import *
from .verity_get import *

class_name = "VeritySense"


class VeritySense(BaseDevice):
    def __init__(self, params):
        self._initialize_device_params(
            ["sessions"],
            params,
            {
                "seed": 0,
                "start_date": "2022-03-01",
                "end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["start_date"],
            "end_date": self.init_params["end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(
            params["start_date"],
            params["end_date"],
            data_type,
            {"email": self.email, "password": self.password},
        )

    def _filter_synthetic(self, data, data_type, params):
        # return data within range of start date and end date
        result = {}
        for key in data.keys():
            if np.datetime64(key) - np.datetime64(params["end_date"]) > 0:
                break
            elif np.datetime64(key) - np.datetime64(params["start_date"]) < 0:
                continue
            else:
                result[key] = data[key]
        return result

    def _gen_synthetic(self):
        # generate heart rate data according to start and end dates
        self.sessions = gen_data(
            self.init_params["start_date"],
            self.init_params["end_date"],
        )

    def authenticate(self, auth_creds):

        # login first not during data extraction
        # set credentials for device object to be accessed later
        self.email = auth_creds["email"]
        self.password = auth_creds["password"]
