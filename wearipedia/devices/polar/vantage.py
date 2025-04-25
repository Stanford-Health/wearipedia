import base64
import re
import uuid
from datetime import datetime

import requests

from ...utils import seed_everything
from ..device import BaseDevice
from .vantage_fetch import fetch_real_data
from .vantage_synthetic import create_syn_data


class PolarVantage(BaseDevice):

    """This device allows you to work with data from the `Polar Vantage <https://www.polar.com/us-en/vantage/v2>`_ device.
    Available datatypes for this device are:

    * `sleep`: a list that contains sleep data for each day

    * `daily_activity`: a list that contains daily activity data for each day

    * `training_data`: a list that contains daily activity data for each day

    * `training_by_id`: a list that contains training data for a given training session

    * `activity_by_id`: a list that contains activity data for a given activity session

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "polar/vantage"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }

        self._initialize_device_params(
            ["sleep", "daily_activity", "training_data", "training_by_id"],
            params,
            {"seed": 0, "start_date": "2022-03-01", "end_date": "2022-06-17"},
        )

        self.token = None
        self.user_id = None

    def _default_params(self):
        return {
            "training_id": None,
            "start_date": self.init_params["start_date"],
            "end_date": self.init_params["end_date"],
        }

    def _get_real(self, data_type, params):
        if "training_id" in params:
            return fetch_real_data(
                self.token,
                self.user_id,
                params["start_date"],
                params["end_date"],
                data_type,
                params["training_id"],
            )
        else:
            return fetch_real_data(
                self.token,
                self.user_id,
                params["start_date"],
                params["end_date"],
                data_type,
                "",
            )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        # convert the dates to datetime objects
        def date_str_to_obj(x):
            return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.training_data, self.sleep, self.training_by_id = create_syn_data(
            self.init_params["start_date"],
            self.init_params["end_date"],
        )
        self.daily_activity = []
        self.activity_by_id = []

    def _authenticate(self, auth_creds=None):
        if (
            auth_creds
            and isinstance(auth_creds, dict)
            and auth_creds.get("access_token")
            and auth_creds.get("user_id")
        ):
            self.token = auth_creds["access_token"]
            self.user_id = auth_creds["user_id"]
            return

        print(
            "Input your client id.",
            "If you need a new application, you can register one at https://admin.polaraccesslink.com",
            "\n",
        )

        client_id = input("Enter the client id: ")
        client_secret = input("Enter the client secret: ")

        # combine all parameters into the url string
        url = f"https://flow.polar.com/oauth2/authorization?response_type=code&client_id={client_id}&scope=accesslink.read_all"

        print(
            "Click the URL above to access the Authorization page. Check Allow All and click the Allow button then input the resulting url",
            url,
        )

        authurl = input("Enter the resulting url: ")

        lst_of_token = []
        append = False
        for i in authurl:
            if i == "=":
                append = True
                continue
            elif i == "&":
                break
            if append == True:
                lst_of_token.append(i)

        authorization_code = "".join(lst_of_token)
        credentials = f"{client_id}:{client_secret}"

        # Encode to base64
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
        }
        body = {
            "grant_type": "authorization_code",
            "code": authorization_code,
        }

        r = requests.post(
            "https://polarremote.com/v2/oauth2/token", data=body, headers=headers
        )
        if r.status_code != 200:
            print("Failed authorization request:", r.json())

        if "access_token" not in r.json():
            print("No access token found:", r.json())

        self.token = r.json()["access_token"]
        self.user_id = r.json()["x_user_id"]
        print("Access token:", self.token)
        print("User ID:", self.user_id)

        input_body = {"member-id": self.user_id}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        r = requests.post(
            "https://www.polaraccesslink.com/v3/users", headers=headers, json=input_body
        )

        if r.status_code >= 200 and r.status_code < 400:
            print("Registered user:")
            print(r.json())
        elif r.status_code != 409:
            print(r)
