import os
import time
import unittest.mock as mock

from tqdm import tqdm

import wearipedia

MAX_DEVICE_TEST_TIME = 15

DEVICE_TO_AUTH_DICT = {
    "garmin/fenix_7s": {
        "email": os.environ["GARMIN_FENIX_7S_EMAIL"],
        "password": os.environ["GARMIN_FENIX_7S_PASSWORD"],
    }
}


def test_all_devices_real():
    # this test emphasizes actually integrating with the real API,
    # so we mainly just check that

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

        device.authenticate(DEVICE_TO_AUTH_DICT[device_name])

        for data_type in device.valid_data_types:
            data = device.get_data(data_type)

            assert data is not None
