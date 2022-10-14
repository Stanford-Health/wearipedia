# content of test_sample.py
import wearipedia


def test_cgm_synthetic():
    device = wearipedia.get_device("dexcom/pro_cgm")

    device.gen_synthetic()

    dataframe = device.get_data("dataframe")
