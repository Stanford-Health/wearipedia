import base64
import json
import os
from pathlib import Path

import requests

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .dreem_fetch import *
from .dreem_gen import *

class_name = "DreemHeadband2"


class DreemHeadband2(BaseDevice):
    def __init__(self, params):
        self._initialize_device_params(
            ["users", "records", "hypnogram", "eeg_file"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        # this is wrong, but it's just a placeholder
        return dict()

    def _get_real(self, data_type, params):
        if data_type == "users":
            return fetch_users(self.auth_dict)
        elif data_type == "records":
            return fetch_records(self.auth_dict, params["user"])
        elif data_type == "hypnogram":
            return fetch_hypnogram(self.auth_dict, params["record_ref"])
        elif data_type == "eeg_file":
            return fetch_eeg_file(self.auth_dict, params["record_ref"])

    def _get_synthetic(self, data_type, params):
        return []

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

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
