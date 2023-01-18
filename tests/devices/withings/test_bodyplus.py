# perform additional test specific to withings bodyplus device

from datetime import datetime

import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_withings_bodyplus_synthetic(real):
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]

    for start_date in start_dates:
        device = wearipedia.get_device(
            "withings/bodyplus",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("withings/bodyplus", device)

        # calling tests for each pair of start dates
        helper_test(device, start_date)


def helper_test(device, start_date):

    measurements = device.get_data("measurements")

    # making sure schema of the measurements dataframe is correct
    assert (
        measurements.columns == ["date", "Weight (kg)", "Fat Ratio (%)"]
    ).all(), f"Measurements data is not correct: {measurements}"

    # check that the generated date is after the start date
    for date in measurements["date"]:
        assert date >= start_date, f"Date is not correct: {date}"

    # check that weight (kg) is in a suitable range
    for weight in measurements["Weight (kg)"]:
        assert 0 <= weight <= 300, f"Weight is not correct: {weight}"

    # check that fat ratio (%) is in a suitable range
    for fat_ratio in measurements["Fat Ratio (%)"]:
        assert 0 <= fat_ratio <= 100, f"Fat ratio is not correct: {fat_ratio}"
