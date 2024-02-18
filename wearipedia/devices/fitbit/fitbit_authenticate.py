import base64
import hashlib
import os

import requests

__all__ = ["login", "fitbit_application", "fitbit_token"]


def fitbit_token():
    """gives us access token given the login info

    :return: access token
    :rtype: str
    """

    access_token = input("Enter your access token: ")

    return access_token
