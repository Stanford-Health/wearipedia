# content of test_sample.py
import wearipedia


def test_sleepmat_synthetic():
    device = wearipedia.get_device("withings/sleepmat")

    device.gen_synthetic()

    measurements = device.get_data("measurements")
