import random
import string
import time
from urllib.parse import parse_qs, urlparse

import requests

__all__ = ["refresh_access_token", "whoop_authenticate"]

CALLBACK_URI = "https://wearipedia.com/"


def whoop_authenticate(client_id: str, client_secret: str) -> tuple:
    """
    Initiates the authentication process for WHOOP API and retrieves access and refresh tokens.

    :param client_id: The client ID for API authentication.
    :type client_id: str

    :param client_secret: The client secret for API authentication.
    :type client_secret: str

    :return: A tuple containing the access token and refresh token. (refresh_token, access_token)
    :rtype: tuple

    :raises Exception: Raised if the authentication process encounters an error.
    """

    authURL = "https://api.prod.whoop.com/oauth/oauth2/auth"
    authURL += "?"
    authURL += (
        "response_type=code&"
        + f"client_id={client_id}&"
        + f"redirect_uri={CALLBACK_URI}&"
        + f"scope=read:recovery%20read:cycles%20read:workout%20read:sleep%20read:profile%20read:body_measurement%20offline&"
    )
    state = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    authURL += f"state={state}"
    authURL = authURL[:-1]

    print("----------------------------")
    print(
        "Authorization url below. Please sign in to grant access, and copy the redirect url."
    )
    print(authURL)
    print("----------------------------")
    print("Enter redirect url:")
    time.sleep(0.1)
    redirect_url = input("> ")

    # Request tokens
    try:
        query_string = urlparse(redirect_url).query
        code = parse_qs(query_string)["code"][0]
    except Exception as e:
        exception_str = f"Caught error:\n{e}\n"
        exception_str += "Please copy and paste the entire URL (including https)"
        raise Exception(exception_str)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": CALLBACK_URI,
    }
    response = requests.post(
        "https://api.prod.whoop.com/oauth/oauth2/token", data=params, headers=headers
    )

    if response.status_code == 200:
        access_token, refresh_token = response.json().get(
            "access_token"
        ), response.json().get("refresh_token")
        print("Authentication succeeded.")

    else:
        print("Error:", response.json().get("error"))
        print("Error Description:", response.json().get("error_description"))

    return refresh_token, access_token


# Refresh tokens
def refresh_access_token(refresh_token, client_id, client_secret):
    """
    Refresh the access token using a refresh token.

    :param refresh_token: The refresh token used to obtain a new access token.
    :type refresh_token: str

    :param client_id: The client ID associated with the application.
    :type client_id: str

    :param client_secret: The client secret associated with the application.
    :type client_secret: str

    :return: A tuple containing the refresh token and new access token obtained from the refresh token. (refresh_token, new_access_token)
    :rtype: tuple
    """
    params = {
        "action": "requesttoken",
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    response = requests.post(
        "https://api.prod.whoop.com/oauth/oauth2/token", data=params
    )
    try:
        new_access_token, refresh_token = response.json().get(
            "access_token"
        ), response.json().get("refresh_token")
        # print("Access Token:", access_token)
        # print("Refresh Token:", refresh_token)
    except:
        print("Error:", response.json().get("error"))
        print("Error Description:", response.json().get("error_description"))

    return refresh_token, new_access_token
