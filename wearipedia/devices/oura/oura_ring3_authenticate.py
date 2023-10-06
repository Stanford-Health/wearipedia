import base64
import hashlib
import os

import requests

__all__ = ["oura_token"]


def oura_token():
    """gives us access token given the login info

    :return: access token
    :rtype: str
    """

    print(
        "fill the login info in this url then generate the token: ",
        "https://cloud.ouraring.com/personal-access-tokens",
        "\n",
    )
    access_token = input("Enter the resulting token: ")

    return access_token
