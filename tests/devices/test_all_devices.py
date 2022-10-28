import wearipedia


def test_all_devices():
    for device_name in wearipedia.get_all_device_names():
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

        # now check which methods have been called at this point

        # now check that the device can return synthetic data
        for data_type in device.valid_data_types:
            data = device.get_data(data_type)
