import os
import time
import unittest.mock as mock

from tqdm import tqdm

import wearipedia

DEVICE_TO_AUTH_DICT = {
    "garmin/fenix_7s": {
        "email": os.environ["GARMIN_FENIX_7S_EMAIL"],
        "password": os.environ["GARMIN_FENIX_7S_PASSWORD"],
    },
    "whoop/whoop_4": {
        "email": os.environ["WHOOP_4_EMAIL"],
        "password": os.environ["WHOOP_4_PASSWORD"],
    },
    "withings/bodyplus": {
        "refresh_token_env_var": "WITHINGS_REFRESH_TOKEN",
        "client_id": os.environ["WITHINGS_CLIENT_ID"],
        "customer_secret": os.environ["WITHINGS_CUSTOMER_SECRET"],
        "refresh_token": os.environ["WITHINGS_REFRESH_TOKEN"],
    },
    "withings/scanwatch": {
        "refresh_token_env_var": "WITHINGS_REFRESH_TOKEN",
        "client_id": os.environ["WITHINGS_CLIENT_ID"],
        "customer_secret": os.environ["WITHINGS_CUSTOMER_SECRET"],
        "refresh_token": os.environ["WITHINGS_REFRESH_TOKEN"],
    },
    "dexcom/pro_cgm": {
        "refresh_token_env_var": "DEXCOM_REFRESH_TOKEN",
        "client_id": os.environ["DEXCOM_CLIENT_ID"],
        "client_secret": os.environ["DEXCOM_CLIENT_SECRET"],
        "refresh_token": os.environ["DEXCOM_REFRESH_TOKEN"],
    },
}


def test_all_devices_real():
    # this test emphasizes actually integrating with the real API,
    # so we mainly just check that

    # TODO: also test that real agrees with synthetic

    pbar = tqdm(
        [
            x
            for x in wearipedia.get_all_device_names()
            if x in DEVICE_TO_AUTH_DICT.keys()
        ]
    )

    for device_name in pbar:
        pbar.set_description(f"Testing {device_name}...")
        device = wearipedia.get_device(device_name)

        auth_dict = DEVICE_TO_AUTH_DICT[device_name]

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

        device.authenticate(auth_dict)

        if "refresh_token" in auth_dict:
            # we're running in GitHub Actions, so we can
            # update the refresh token
            refresh_token_env_var = DEVICE_TO_AUTH_DICT[device_name][
                "refresh_token_env_var"
            ]

            os.environ[refresh_token_env_var] = device.refresh_token

        for data_type in device.valid_data_types:
            data = device.get_data(data_type)

            assert data is not None
