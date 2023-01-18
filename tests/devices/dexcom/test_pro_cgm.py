# perform additional test specific to dexcom pro CGM device

from datetime import datetime

import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_dexcom_pro_cgm(real):
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "dexcom/pro_cgm",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("dexcom/pro_cgm", device)

        # calling tests for each pair of start and end dates
        helper_test(device, start_date, end_date)


def helper_test(device, start_date, end_date):

    data = device.get_data(
        "data",
        {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        },
    )

    assert list(data.keys()) == [
        "unit",
        "rateUnit",
        "egvs",
    ], f'top-level keys are not correct: {list(data.keys())}, expected ["unit", "rateUnit", "egvs"]'

    egvs_type = type(data["egvs"])

    assert egvs_type == type([]), f"expected egvs to be a list, got {egvs_type}"

    if len(data["egvs"]) > 0:
        assert list(data["egvs"][0].keys()) == [
            "systemTime",
            "displayTime",
            "value",
            "realtimeValue",
            "smoothedValue",
            "status",
            "trend",
            "trendRate",
        ]

        # TODO: add more checks
        for egv in data["egvs"]:
            val, realtimeval = egv["value"], egv["realtimeValue"]
            assert (
                50 <= val <= 200
            ), f"Expected glucose values to be between 50 and 200, got {val}"
            assert (
                50 <= realtimeval <= 200
            ), f"Expected glucose values to be between 50 and 200, got {realtimeval}"
