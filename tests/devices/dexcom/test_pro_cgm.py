# perform additional test specific to dexcom pro CGM device

from datetime import datetime

import wearipedia


def test_dexcom_pro_cgm():
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "dexcom/pro_cgm",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        # calling tests for each pair of start and end dates
        helper_test(device, start_date, end_date)


def helper_test(device, start_date, end_date):

    dataframe = device.get_data("dataframe")

    # making sure schema of the dataframe is correct
    assert (
        dataframe.columns == ["datetime", "glucose_level"]
    ).all(), f"Dataframe data is not correct: {measurements}"

    # check that the generated date is after the start date
    for date in dataframe["datetime"]:
        assert date >= start_date, f"Date is not correct: {date}"

    # check that generated date is before end date
    for date in dataframe["datetime"]:
        assert date <= end_date, f"Date is not correct: {date}"

    # check that glucose level is in a suitable range
    for weight in dataframe["glucose_level"]:
        assert 0 <= weight <= 500, f"Weight is not correct: {weight}"
