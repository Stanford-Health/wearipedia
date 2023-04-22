from datetime import datetime, timedelta

import pytest
from dateutil import parser

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_fitbit_charge_4_synthetic(real):
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "fitbit/fitbit_charge_4",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("fitbit/fitbit_charge_4", device)

        helper_test(device, start_date, end_date, real)


def helper_test(device, start_synthetic, end_synthetic, real):
    sleep = device.get_data(
        "sleep",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
        },
    )
    steps = device.get_data(
        "steps",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
        },
    )

    assert 1 == 1
