# content of test_sample.py
import wearipedia


def test_scan_watch_synthetic():
    device = wearipedia.get_device("withings/scanwatch")

    heart_rates = device.get_data("heart_rates")

    sleeps = device.get_data("sleeps")
