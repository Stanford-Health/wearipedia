# content of test_sample.py
import wearipedia


def test_fenix_synthetic():
    device = wearipedia.get_device("garmin/fenix_7s")

    device.gen_synthetic()

    dates = device.get_data("dates")

    steps = device.get_data("steps")

    hrs = device.get_data("hrs")

    brpms = device.get_data("brpms")
