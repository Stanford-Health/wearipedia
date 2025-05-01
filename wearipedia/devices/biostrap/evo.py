import os
import pickle
import webbrowser
from datetime import datetime
from urllib.parse import urlencode

import requests

from ...utils import seed_everything
from ..device import BaseDevice
from .evo_fetch import fetch_real_data
from .evo_gen import create_syn_data


class EVO(BaseDevice):

    name = "biostrap/evo"

    def __init__(self, seed=0, start_date="2023-06-05", end_date="2023-06-20"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }

        self._initialize_device_params(
            [
                "activities",
                "bpm",
                "brpm",
                "hrv",
                "spo2",
                "rest_cals",
                "work_cals",
                "active_cals",
                "step_cals",
                "total_cals",
                "sleep_session",
                "sleep_detail",
                "steps",
                "distance",
            ],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2023-06-05",
                "synthetic_end_date": "2023-06-20",
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(
            self.access_token, params["start_date"], params["end_date"], data_type
        )

    def _filter_synthetic(self, data, data_type, params):
        start_date = params["start_date"]
        end_date = params["end_date"]

        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"

        # For data types that are stored with a date string as a key
        if data_type in [
            "rest_cals",
            "work_cals",
            "active_cals",
            "step_cals",
            "total_cals",
        ]:
            return {
                date: value
                for date, value in data.items()
                if start_date <= date <= end_date
            }

        # For data types that are stored with a datetime string as a key in a tuple
        elif data_type in [
            "bpm",
            "brpm",
            "spo2",
            "hrv",
        ]:
            return {
                key: value
                for key, value in data.items()
                if start_datetime <= key[0] <= end_datetime
            }

        # For steps and distance that use datetime strings as keys (assuming distance also has datetime as per steps)
        elif data_type in ["steps", "distance"]:
            return {
                datetime: value
                for datetime, value in data.items()
                if start_datetime <= datetime <= end_datetime
            }

        else:
            return data

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])
        # and based on start and end dates
        (
            self.activities,
            self.bpm,
            self.brpm,
            self.hrv,
            self.spo2,
            self.rest_cals,
            self.work_cals,
            self.active_cals,
            self.step_cals,
            self.total_cals,
            self.sleep_session,
            self.sleep_detail,
            self.steps,
            self.distance,
        ) = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    # We get the access token to make requests to the Biostrap API
    def _authenticate(self, auth_creds):
        self.client_id = auth_creds["client_id"]
        self.client_secret = auth_creds["client_secret"]
        redirect_uri = "https://127.0.0.1:8080"
        token_url = "https://auth.biostrap.com/token"

        # Generate the authorization URL and open it in the default web browser
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
        }
        authorization_url = f"https://auth.biostrap.com/authorize?{urlencode(params)}"

        # Instruct the user to open the URL in their browser ()
        print(
            f"Please go to the following URL and authorize access: {authorization_url}"
        )
        print(
            "If a page cannot be displayed, please make sure you are logged into the Biostrap account in your browser."
        )

        # Get the authorization response URL from the command line (the method Jack and I talked about didn't work)
        authorization_response = input("Enter the full callback URL: ")

        code = authorization_response.split("code=")[1].split("&")[0]

        # Now we can request the access token
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        auth = (self.client_id, self.client_secret)
        response = requests.post(token_url, auth=auth, data=data)

        # Get the access token from the response
        token_json = response.json()
        self.access_token = token_json["access_token"]
