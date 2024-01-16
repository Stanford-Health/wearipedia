from datetime import datetime, timedelta

import pytest

import wearipedia

data_formats = {
    "bpm": (int, float),
    "brpm": (int, float),
    "hrv": (int, float),
    "spo2": (int, float),
    "rest_cals": (int, float),
    "work_cals": (int, float),
    "active_cals": (int, float),
    "step_cals": (int, float),
    "total_cals": (int, float),
    "steps": (int, float),
    "distance": (int, float),
}


@pytest.mark.parametrize("real", [True, False])
def test_evo(real):
    start_synthetic = datetime(2023, 6, 5)
    end_synthetic = datetime(2023, 6, 20, 23, 59, 59)

    device = wearipedia.get_device(
        "biostrap/evo",
        start_date=datetime.strftime(start_synthetic, "%Y-%m-%d"),
        end_date=datetime.strftime(end_synthetic, "%Y-%m-%d"),
    )
    if real:
        wearipedia._authenticate_device("evo", device)

    for data_type, data_format in data_formats.items():
        data = device.get_data(data_type)

        # Checks specific to date-keyed data
        if data_type in [
            "rest_cals",
            "work_cals",
            "active_cals",
            "step_cals",
            "total_cals",
        ]:
            dates = list(data.keys())

            # Check dates are consecutive and within the range
            expected_date = start_synthetic
            for date_str in dates:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                assert (
                    date == expected_date
                ), f"Expected date {expected_date}, but got {date}"
                expected_date += timedelta(days=1)

        # Checks specific to datetime-keyed data
        elif data_type in ["steps", "distance"]:

            datetimes = [
                datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") for dt_str in data.keys()
            ]

            # Check that datetimes are within the specified range.
            for dt in datetimes:
                assert (
                    start_synthetic <= dt <= end_synthetic
                ), f"Datetime {dt} out of range"

            # Check that the datetimes are sequential and increase by a minute.
            datetimes.sort()
            for i in range(1, len(datetimes)):
                expected_dt = datetimes[i - 1] + timedelta(minutes=1)
                assert (
                    datetimes[i] == expected_dt
                ), f"Expected datetime {expected_dt}, but got {datetimes[i]}"
        else:
            datetimes = [key[0] for key in data.keys()]

            # Check datetimes are within the range
            for datetime_str in datetimes:
                dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                assert (
                    start_synthetic <= dt <= end_synthetic
                ), f"Datetime {dt} out of range"

        # Check data values are of expected type
        for value in data.values():
            assert isinstance(
                value, data_format
            ), f"{data_type} data {value} is not a {data_format.__name__}"
