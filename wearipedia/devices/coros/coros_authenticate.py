import base64
import hashlib
import os

import requests

__all__ = ["login"]


def login(email, password):
    if len(email) == 0:  # fake the login
        token = ""
        user_id = ""
    else:
        login = requests.post(
            "https://accounts.fitbit.com/login",
            json={
                "grant_type": "password",
                "issueRefresh": False,
                "password": password,
                "username": email,
            },
        )

    return token
