import wearipedia


def test_cgm_synthetic():
    device = wearipedia.get_device("dexcom/pro_cgm")

    dataframe = device.get_data("dataframe")
