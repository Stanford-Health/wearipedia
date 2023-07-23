import os
import pickle
import webbrowser
from datetime import datetime
from urllib.parse import urlencode

import requests

from ...utils import seed_everything
from ..device import BaseDevice
from .evo_fetch import *
from .evo_gen import *

class_name = "EVO"


class EVO(BaseDevice):
    def __init__(self, seed=0, start_date="2023-06-05", end_date="2023-06-20"):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }

        self._initialize_device_params(
            ["steps", "calories", "bpm", "brpm", "spo2"],
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
        return data

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.steps, self.calories, self.bpm, self.brpm, self.spo2 = create_syn_data(
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
        webbrowser.open(authorization_url)

        # Get the authorization response URL from the command line: is there a better way to do this?
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
