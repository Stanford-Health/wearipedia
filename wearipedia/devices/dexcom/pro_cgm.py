import http
import json
import time
import urllib

import numpy as np
import pandas as pd

from ...devices.device import BaseDevice
from ...utils import bin_search, seed_everything
from .pro_cgm_fetch import *
from .pro_cgm_gen import *

class_name = "DexcomProCGM"


class DexcomProCGM(BaseDevice):
    def __init__(self, params):
        self._initialize_device_params(
            ["dataframe"],
            params,
            {"seed": 0, "synthetic_start": "2022-02-16", "synthetic_end": "2022-05-15"},
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start"],
            "end_date": self.init_params["synthetic_end"],
        }

    def _get_real(self, data_type, params):
        # there is really only one data type for this device,
        # so we don't need to check the data_type

        return fetch_data(
            self.access_token,
            start_date=params["start_date"],
            end_date=params["end_date"],
        )

    def _filter_synthetic(self, data, data_type, params):
        # there is really only one data type for this device,
        # so we don't need to check the data_type

        start_ts = pd.Timestamp(params["start_date"])
        end_ts = pd.Timestamp(params["end_date"])

        start_idx = bin_search(np.array(self.dataframe.datetime), start_ts)
        end_idx = bin_search(np.array(self.dataframe.datetime), end_ts)

        return self.dataframe.iloc[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        self.dataframe = create_synth_df(
            self.init_params["synthetic_start"], self.init_params["synthetic_end"]
        )

    def _authenticate(self, auth_creds, use_cache=True):
        if use_cache and hasattr(self, "access_token"):
            return

        your_client_secret = auth_creds["client_secret"]
        your_client_id = auth_creds["client_id"]
        your_redirect_uri = "https://www.google.com"  # @param {type:"string"}
        your_state_value = "1234"

        url = f"https://api.dexcom.com/v2/oauth2/login?client_id={your_client_id}&redirect_uri={your_redirect_uri}&response_type=code&scope=offline_access&state={your_state_value}"

        print(url)

        print("redirect url below:")
        time.sleep(0.1)
        redirect_url = input(">")

        try:
            your_authorization_code = urllib.parse.parse_qs(
                urllib.parse.urlparse(redirect_url).query
            )["code"][0]
        except Exception as e:
            print(f"Caught error:\n{e}\n")
            print("Please copy and paste the entire URL (including https)")

        conn = http.client.HTTPSConnection("api.dexcom.com")

        payload = f"client_secret={your_client_secret}&client_id={your_client_id}&code={your_authorization_code}&grant_type=authorization_code&redirect_uri={your_redirect_uri}"

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }

        conn.request("POST", "/v2/oauth2/token", payload, headers)

        res = conn.getresponse()
        data = res.read()

        json_response = json.loads(data.decode("utf-8"))

        if (
            "error" in json_response.keys()
            and json_response["error"] == "invalid_grant"
        ):
            print("The code you got has expired.")
            print("Authorize and enter the redirect URL again.")
        else:
            access_token = json.loads(data.decode("utf-8"))["access_token"]

            print(f'Entire response was {data.decode("utf-8")}')
            print(f"Our access token is {access_token}")

        self.access_token = access_token
