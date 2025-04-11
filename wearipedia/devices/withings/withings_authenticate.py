import json
import time
import urllib

import requests

__all__ = ["refresh_access_token", "withings_authenticate"]

STATE = "string"
ACCOUNT_URL = "https://account.withings.com"
CALLBACK_URI = "https://wbsapi.withings.net/v2/oauth2"


def refresh_access_token(refresh_token, client_id, client_secret):
    # gives us access token given the refresh token

    params = {
        "action": "requesttoken",
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    out = requests.post("https://wbsapi.withings.net/v2/oauth2", data=params)

    try:
        body = json.loads(out.text)["body"]
        new_refresh_token, access_token = body["refresh_token"], body["access_token"]
        print(f"Got new refresh token: {new_refresh_token}")
    except KeyError as e:
        exception_str = f"Got exception: {e}\n"
        exception_str += f"The full returned payload is: {json.loads(out.text)}"
        raise Exception(exception_str)

    return new_refresh_token, access_token


def withings_authenticate(client_id, client_secret):
    # gives us access token given the auth_creds + going through the process, it's interactive

    payload = {
        "response_type": "code",  # imposed string by the api
        "client_id": client_id,
        "state": STATE,
        "scope": "user.info,user.metrics,user.activity",  # see docs for enhanced scope
        "redirect_uri": CALLBACK_URI,  # URL of this app
        #'mode': 'demo'  # Use demo mode, DELETE THIS FOR REAL APP
    }

    url = f"{ACCOUNT_URL}/oauth2_user/authorize2?"

    for key, value in payload.items():
        url += f"{key}={value}&"

    url = url[:-1]

    print(url)
    print("Enter the redirect url below:")
    time.sleep(0.1)
    redirect_url = input(">")

    try:
        code = urllib.parse.parse_qs(urllib.parse.urlparse(redirect_url).query)["code"][
            0
        ]
    except Exception as e:
        exception_str = f"Caught error:\n{e}\n"
        exception_str += "Please copy and paste the entire URL (including https)"
        raise Exception(exception_str)

    params = {
        "action": "requesttoken",
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        #'scope': 'user.info',
        "redirect_uri": "https://wbsapi.withings.net/v2/oauth2",
    }

    out = requests.get("https://wbsapi.withings.net/v2/oauth2", data=params)

    out = json.loads(out.text)

    try:
        refresh_token, access_token = (
            out["body"]["refresh_token"],
            out["body"]["access_token"],
        )
    except KeyError as e:
        raise Exception("Took too long to paste in redirect URL. Please repeat step 7.")

    print("Refresh token:", refresh_token)
    print("Access token:", access_token)

    return refresh_token, access_token
