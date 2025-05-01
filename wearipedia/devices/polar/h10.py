import numpy as np
import requests

from ...devices.device import BaseDevice
from .h10_gen import gen_data
from .polar_get import fetch_real_data


class H10(BaseDevice):
    """This device allows you to work with data from the `Polar H10 <https://www.polar.com/us-en/sensors/h10-heart-rate-sensor>`_ device.
    Available datatypes for this device are:

    * `sessions`: contains data from all sessions in one

    * `rr`: contains data from all rr sessions in one

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type start_date: str, optional
    :param end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type end_date: str, optional
    """

    name = "polar/h10"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):

        params = {
            "seed": seed,
            "start_date": start_date,
            "end_date": end_date,
        }

        self._initialize_device_params(
            ["sessions", "rr"],
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
            self.elite_hrv_session,
        )

    def _filter_synthetic(self, data, data_type, params):
        # return data within range of start date and end date
        # includes both RR and HR data
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
        self.rr, self.sessions = gen_data(
            self.init_params["seed"],
            self.init_params["start_date"],
            self.init_params["end_date"],
        )

    def _authenticate(self, auth_creds):
        self.elite_hrv_session = None
        self.session = None
        self.post = None

        # check if auth_creds has email and password
        if "email" in auth_creds and "password" in auth_creds:
            # set credentials for device object to be accessed later if needed
            email = auth_creds["email"]
            password = auth_creds["password"]

            # authenticate device in a python session and save it
            auth = {"email": email, "password": password}
            self.session = requests.Session()

            # contains polar global variables we need later
            self.post = self.session.post("https://flow.polar.com/login", data=auth)

        # check if eliteHRV credentials exist
        if "elite_hrv_email" in auth_creds and "elite_hrv_password" in auth_creds:
            elite_hrv_email = auth_creds["elite_hrv_email"]
            elite_hrv_password = auth_creds["elite_hrv_password"]

            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://dashboard.elitehrv.com",
                "Referer": "https://dashboard.elitehrv.com/",
            }
            data = f"email={elite_hrv_email}%40gmail.com&password={elite_hrv_password}&version=*&locale=en-us&language=en"

            # authenticate device in a python session and save it
            response = requests.post(
                "https://app.elitehrv.com/application/index/login",
                headers=headers,
                data=data,
            )
            self.elite_hrv_session = response.json()
