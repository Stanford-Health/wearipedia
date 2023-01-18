import json
import os
import time
import unittest.mock as mock
from pathlib import Path

from tqdm import tqdm

import wearipedia


def test_all_devices_real():
    # this test emphasizes actually integrating with the real API,
    # so we mainly just check that

    pbar = tqdm(
        [
            x
            for x in wearipedia.get_all_device_names()
            if x in wearipedia._DEVICE_TO_AUTH_DICT.keys()
        ]
    )

    for device_name in pbar:
        pbar.set_description(f"Testing {device_name}...")
        device = wearipedia.get_device(device_name)

        auth_dict = wearipedia._DEVICE_TO_AUTH_DICT[device_name]

        # if we have a refresh token and we're running in
        # GitHub Actions, then we can use the refresh token
        # and then set a GitHub secret to the returned refresh
        # token to keep things up to date (this happens later
        # with something like this:
        # https://github.com/marketplace/actions/create-github-secret-action)

        # on the other hand, if we have a refresh token and
        # we're not running in GitHub Actions, then we can use
        # the refresh token and then set the corresponding local
        # environment variable to the returned refresh token to
        # keep things up to date, keeping in mind that the updated
        # refresh token needs to be later set as a GitHub secret

        # this is because according to OAuth 2.0, the refresh token
        # is only supposed to be used once, so we need to update
        # it every time we use it

        wearipedia._authenticate_device(device_name, device)

        # replace with refresh token json on disk if possible
        # disk_refresh_token = wearipedia.read_refresh_token_from_json(device_name)
        # if disk_refresh_token is not None:
        #    auth_dict["refresh_token"] = disk_refresh_token

        # device.authenticate(auth_dict)

        for data_type in device.valid_data_types:
            data = device.get_data(data_type)

            assert data is not None
