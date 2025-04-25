from datetime import datetime

import requests

from ...utils import seed_everything
from ..device import BaseDevice
from .googlefitness_fetch import fetch_real_data
from .googlefitness_synthetic import create_syn_data


class GoogleFit(BaseDevice):

    """This device allows you to work with data from the `Google Fit <https://www.google.com/fit/>`_ app.
    Available datatypes for this device are:

    * `steps`: a list that contains total steps walked for each day

    * `heart_rate`: a list that contains heart rate data for each day

    * `sleep`: a list that contains sleep data for each day

    * `heart_minutes`: a list that contains heart minutes data for each day

    * `blood_pressure`: a list that contains blood pressure data for each day

    * `blood_glucose`: a list that contains blood glucose data for each day

    * `body_temperature`: a list that contains body temperature data for each day

    * `calories_expended`: a list that contains calories expended data for each day

    * `activity_minutes`: a list that contains activity minutes data for each day

    * `height`: a list that contains height data for each day

    * `oxygen_saturation`: a list that contains oxygen saturation data for each day

    * `menstruation`: a list that contains menstruation data for each day

    * `speed`: a list that contains speed data for each day

    * `weight`: a list that contains weight data for each day

    * `distance`: a list that contains distance data for each day

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "google/googlefit"

    def __init__(self, seed=0, start_date="2022-03-01", end_date="2022-06-17"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }

        self._initialize_device_params(
            [
                "steps",
                "heart_rate",
                "sleep",
                "heart_minutes",
                "blood_pressure",
                "blood_glucose",
                "body_temperature",
                "calories_expended",
                "activity_minutes",
                "height",
                "oxygen_saturation",
                "menstruation",
                "speed",
                "weight",
                "distance",
            ],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "time_bucket": "86400000",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
            "time_bucket": self.init_params["time_bucket"],
        }

    def _get_real(self, data_type, params):
        if "time_bucket" not in params:
            return fetch_real_data(
                self, params["start_date"], params["end_date"], data_type
            )
        return fetch_real_data(
            self,
            params["start_date"],
            params["end_date"],
            data_type,
            params["time_bucket"],
        )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        def date_str_to_obj(x):
            return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])
        # steps, hrs, weight, height, speed, heart_minutes, calories_expended, sleep,
        #  blood_pressure, blood_glucose, activity_mins, distance, oxygen_saturation,
        # body_temperature, menstruation

        # # and based on start and end dates
        (
            self.steps,
            self.heart_rate,
            self.weight,
            self.height,
            self.speed,
            self.heart_minutes,
            self.calories_expended,
            self.sleep,
            self.blood_pressure,
            self.blood_glucose,
            self.activity_minutes,
            self.distance,
            self.oxygen_saturation,
            self.body_temperature,
            self.menstruation,
        ) = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
            self.init_params["time_bucket"],
        )

    def _authenticate(self, auth_creds):

        if "authorization_code" not in auth_creds and "access_token" not in auth_creds:
            raise ValueError(
                "Neither authorization_code nor access_token not found in credentials"
            )

        if "authorization_code" in auth_creds:
            # The exchange_auth_url specifies the URL to the endpoint that exchanges the authorization code for an access token
            exchange_auth_url = (
                "https://developers.google.com/oauthplayground/exchangeAuthCode"
            )

            payload = {
                "token_uri": "https://oauth2.googleapis.com/token",
                "code": auth_creds["authorization_code"],
            }

            # POST request to get the participant's ACCESS TOKEN
            res = requests.post(exchange_auth_url, json=payload)

            # saving the participant's ACCESS TOKEN
            if res.status_code == 200:
                try:
                    self.access_token = res.json()["access_token"]
                    print(
                        "Successfully generated your access token. It will remain valid for an hour. \nYour access token is:"
                        + self.access_token
                    )
                except:
                    raise Exception(
                        "Authentication failed!, please make sure you have a valid authorization code"
                    )
            else:
                raise Exception("Authentication failed!")

        if "access_token" in auth_creds and "authorization_code" not in auth_creds:
            self.access_token = auth_creds["access_token"]

        # The acces token that enables us to access the user's data using google's API
        g_access_token = self.access_token

        # The auth_url specifies the URL to the endpoint that authenticates user credentials
        auth_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources"

        # headers sends the user's credentials to the API during POST request
        headers = {
            "Authorization": f"Bearer {g_access_token}",
            "Content-Type": "application/json;encoding=utf-8",
        }

        # POST request to get the participant's ACCESS TOKEN
        res = requests.get(auth_url, headers=headers)

        # saving the participant's ACCESS TOKEN
        if res.status_code == 200:
            self.access_token = g_access_token
            print("Authenticated!\n")
        else:
            raise Exception("Authentication failed!")

        # figure out how to cache this, considering I am not using an API
        # pickle.dump(self, open(CRED_CACHE_PATH, "wb"))
