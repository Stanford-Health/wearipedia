# content of test_sample.py
import wearipedia


def test_bodyplus_synthetic():
    device = wearipedia.get_device("withings/bodyplus")

    measurements = device.get_data("measurements")
