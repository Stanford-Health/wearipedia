import numpy as np
import requests

from ...devices.device import BaseDevice
from .polar_get import fetch_real_data
from .verity_gen import gen_data


class VeritySense(BaseDevice):
    """This device allows you to work with data from the `Polar Verity Sense <https://www.polar.com/us-en/products/accessories/polar-verity-sense>`_ device.
    Available datatypes for this device are:

    * `sessions`: contains data from all sessions in one

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type start_date: str, optional
    :param end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type end_date: str, optional
    """

    name = "polar/verity_sense"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):

        params = {
            "seed": seed,
            "start_date": start_date,
            "end_date": end_date,
        }

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
            self.session,
            self.post,
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
            self.init_params["seed"],
            self.init_params["start_date"],
            self.init_params["end_date"],
        )

    def _authenticate(self, auth_creds):

        # set credentials for device object to be accessed later if needed
        self.email = auth_creds["email"]
        self.password = auth_creds["password"]

        # authenticate device in a python session and save it
        auth = {"email": self.email, "password": self.password}
        self.session = requests.Session()

        # contains polar global variables we need later
        self.post = self.session.post("https://flow.polar.com/login", data=auth)
