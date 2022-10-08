import os
from pathlib import Path

import wget

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .dreem_fetch import *
from .dreem_gen import *

class_name = "DreemHeadband2"


class DreemHeadband2(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = ["users", "records", "hypnogram", "eeg_file"]

    def _get_data(self, data_type, params=None):
        if hasattr(self, data_type):
            return getattr(self, data_type)

        if data_type == "users":
            return fetch_users(self.auth_dict)
        elif data_type == "records":
            return fetch_records(self.auth_dict, params["user"])
        elif data_type == "hypnogram":
            return fetch_hypnogram(self.auth_dict, params["record_ref"])
        elif data_type == "eeg_file":
            return fetch_eeg_file(self.auth_dict, params["record_ref"])

    def gen_synthetic(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

        # @title Enter login credentials

        import base64
        import json

        import requests

        authorization_str = (
            "Basic "
            + base64.b64encode(
                bytes(auth_creds["email"] + ":" + auth_creds["password"], "utf-8")
            ).decode()
        )

        self.auth_dict = json.loads(
            requests.post(
                "https://login.rythm.co/token/",
                headers={"Authorization": authorization_str},
            ).text
        )

        self._authenticated = True
