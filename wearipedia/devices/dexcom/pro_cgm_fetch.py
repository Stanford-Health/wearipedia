import json
import time
import urllib
from datetime import datetime

import pandas as pd
import requests

__all__ = ["refresh_access_token", "dexcom_authenticate", "fetch_data"]


def refresh_access_token(refresh_token, client_id, client_secret):
    # gives us access token given the refresh token
    raise NotImplementedError


def dexcom_authenticate(your_client_id, your_client_secret):
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

    if "error" in json_response.keys() and json_response["error"] == "invalid_grant":
        print("The code you got has expired.")
        print("Authorize and enter the redirect URL again.")
    else:
        access_token = json.loads(data.decode("utf-8"))["access_token"]

        print(f'Entire response was {data.decode("utf-8")}')
        print(f"Our access token is {access_token}")

    return refresh_token, access_token


def fetch_data(access_token, start_date="2022-02-16", end_date="2022-05-15"):
    start_date = start_date + "T15:30:00"
    end_date = end_date + "T15:45:00"

    headers = {"authorization": f"Bearer {access_token}"}

    endpoint = f"https://api.dexcom.com/v2/users/self/egvs?startDate={start_date}&endDate={end_date}"

    out = json.loads(requests.get(endpoint, headers=headers).text)

    if "errors" in out.keys():
        print(f'Got error(s) {out["errors"]}. Fix start and end dates and rerun.')
    elif "fault" in out.keys():
        print(
            f'Got fault {out["fault"]}. You might need to request another access token.'
        )
    else:

        def dt_string_to_obj(dt_str):
            # converts string like "2022-04-10T10:13:00" to a datetime object
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

        data_dict = [
            {
                "datetime": dt_string_to_obj(x["displayTime"]),
                "glucose_level": x["realtimeValue"],
            }
            for x in out["egvs"][::-1]
        ]

        df = pd.DataFrame.from_dict(data_dict)

        return df
