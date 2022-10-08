import json
import time
import urllib

import requests

__all__ = ["withings_authenticate"]


def withings_authenticate(auth_creds):
    # gives us access token given the auth_creds + going through the process, it's interactive

    # @title 6. Enter your credentials below (from the application you just created)
    CLIENT_ID = auth_creds["client_id"]
    CUSTOMER_SECRET = auth_creds["customer_secret"]

    STATE = "string"
    ACCOUNT_URL = "https://account.withings.com"
    CALLBACK_URI = "https://wbsapi.withings.net/v2/oauth2"

    payload = {
        "response_type": "code",  # imposed string by the api
        "client_id": CLIENT_ID,
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
    # @title 7. Copy and paste the URL you were redirected to below
    # redirect_url = "https://wbsapi.withings.net/v2/oauth2?code=e46275ce54994fa6e6eadc50cd4dd45467c01e0e&state=string"
    print("redirect url below:")
    time.sleep(0.1)
    redirect_url = input(">")

    try:
        code = urllib.parse.parse_qs(urllib.parse.urlparse(redirect_url).query)["code"][
            0
        ]
    except Exception as e:
        print(f"Caught error:\n{e}\n")
        print("Please copy and paste the entire URL (including https)")

    params = {
        "action": "requesttoken",
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CUSTOMER_SECRET,
        "code": code,
        #'scope': 'user.info',
        "redirect_uri": "https://wbsapi.withings.net/v2/oauth2",
    }

    out = requests.get("https://wbsapi.withings.net/v2/oauth2", data=params)

    out = json.loads(out.text)

    try:
        access_token = out["body"]["access_token"]
    except KeyError as e:
        print("Took too long to paste in redirect URL. Please repeat step 7.")

    return access_token
