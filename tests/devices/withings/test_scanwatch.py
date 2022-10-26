# content of test_sample.py
import wearipedia


def test_scan_watch_synthetic():
    device = wearipedia.get_device("withings/scanwatch")

    measurements = device.get_data("measurements")
