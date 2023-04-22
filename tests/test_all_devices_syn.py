import time
import unittest.mock as mock

from tqdm import tqdm

import wearipedia

MAX_DEVICE_TEST_TIME = 15


def test_all_devices():
    pbar = tqdm(wearipedia.get_all_device_names())

    for device_name in pbar:
        device_start_time = time.time()
        pbar.set_description(f"Testing {device_name}...")
        device = wearipedia.get_device(device_name)

        # check member attributes first
        assert (
            len(device.valid_data_types) > 0
        ), f"{device_name} has no valid data types"
        assert (
            not device.authenticated
        ), f"{device_name} is already authenticated somehow"
        assert (
            not device.synthetic_has_been_generated
        ), f"{device_name} has already generated synthetic data somehow"
        assert (
            len(device.init_params) > 0
        ), f"{device_name} has no init params, should have at least a random seed"

        # It's a bit ugly, but we mock all the relevant methods and check
        # that they're called the correct number of times.
        # This is essentially checking that the child class has re-implemented
        # the methods correctly.
        print(device_name)
        with mock.patch.object(
            device.__class__, "_filter_synthetic", wraps=device._filter_synthetic
        ) as mock_get_synthetic, mock.patch.object(
            device.__class__, "_gen_synthetic", wraps=device._gen_synthetic
        ) as mock_gen_synthetic, mock.patch.object(
            device.__class__, "_default_params", wraps=device._default_params
        ) as mock_default_params, mock.patch.object(
            device.__class__, "_get_real", wraps=device._get_real
        ) as mock_get_real, mock.patch.object(
            device.__class__, "authenticate", wraps=device.authenticate
        ) as mock_authenticate:
            for data_type in device.valid_data_types:
                data = device.get_data(data_type)

                mock_gen_synthetic.assert_called_once()

                mock_get_synthetic.assert_called_once()
                mock_get_synthetic.reset_mock()
                mock_default_params.assert_called_once()
                mock_default_params.reset_mock()

                mock_get_real.assert_not_called()
                mock_authenticate.assert_not_called()

        assert time.time() - device_start_time < MAX_DEVICE_TEST_TIME, (
            f"{device_name} took too long to test, expected less than {MAX_DEVICE_TEST_TIME}"
            f" seconds but took {time.time() - device_start_time:.2f} seconds. This is probably"
            "because your device generates synthetic data inefficiently. Try to make it faster."
        )
