import http
import json
import time
import urllib

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .pro_cgm_fetch import *
from .pro_cgm_gen import *

class_name = "DexcomProCGM"


class DexcomProCGM(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = ["dataframe"]

    def _get_data(self, data_type, params=None):
        if params is None:
            params = {"start_date": "2022-02-16", "end_date": "2022-05-15"}

        if self.authenticated:
            return fetch_data(
                self.access_token,
                start_date=params["start_date"],
                end_date=params["end_date"],
            )
        else:
            if hasattr(self, data_type):
                return getattr(self, data_type)
            else:
                raise Exception(
                    "Expected synthetic data to be created, but it hasn't yet."
                )

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

        self.dataframe = create_synth_df()

    def authenticate(self, auth_creds, use_cache=True):
        if use_cache and hasattr(self, "access_token"):
            return

        self.auth_creds = auth_creds

        your_client_secret = auth_creds[
            "client_secret"
        ]  # "NtWS1ViwrO9zuNkZ" #@param {type:"string"}
        your_client_id = auth_creds[
            "client_id"
        ]  # "n92KUDE2pumPUO4u3FStNhKmmpUaV7Gw" #@param {type:"string"}
        your_redirect_uri = "https://www.google.com"  # @param {type:"string"}
        your_state_value = "1234"

        url = f"https://api.dexcom.com/v2/oauth2/login?client_id={your_client_id}&redirect_uri={your_redirect_uri}&response_type=code&scope=offline_access&state={your_state_value}"

        print(url)

        print("redirect url below:")
        time.sleep(0.1)
        redirect_url = input(">")

        # @title Copy the URL into the text box below
        # redirect_url = "https://www.google.com/?code=6fa48a835c032d81eba4991963106771&state=1234" #@param {type:"string"}

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

        self._authenticated = True
