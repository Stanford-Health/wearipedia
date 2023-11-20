# perform additional test specific to HealthKit

from datetime import datetime

import pytest

import wearipedia


@pytest.mark.parametrize("real", [False])
def test_healthkit(real):
    # first test with default params

    start_synthetic = datetime(2021, 1, 1)
    end_synthetic = datetime(2021, 3, 18)

    device = wearipedia.get_device(
        "apple/healthkit",
        synthetic_start_date=datetime.strftime(start_synthetic, "%Y-%m-%d"),
        synthetic_end_date=datetime.strftime(end_synthetic, "%Y-%m-%d"),
    )

    dates = device.get_data("dates")
    steps = device.get_data("steps")
    hrs = device.get_data("hrs")

    assert (
        len(dates) == len(steps) == len(hrs) == (end_synthetic - start_synthetic).days
    ), (
        f"Expected all data to be the same length and to match the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(dates)}, {len(steps)}, {len(hrs)}"
    )

    # first make sure that the dates are correct
    for date_1, date_2 in zip(dates[:-1], dates[1:]):
        assert (
            date_2 - date_1
        ).days == 1, f"Dates are not consecutive: {date_1}, {date_2}"

    assert dates[0] == start_synthetic, f"First date is not correct: {dates[0]}"

    # Now make sure that the steps are correct. We're not going overboard with the
    # tests here, but we're just making sure that the data is in the right ballpark.
    for step_day in steps:
        for step in step_day:
            assert set(step.keys()) == {
                "startGMT",
                "endGMT",
                "steps",
                "primaryActivityLevel",
                "activityLevelConstant",
            }, f"Step data is not correct: {step}"

    # Now make sure that the hrs are correct.
    for hr in hrs:
        assert set(hr.keys()) == {
            "userProfilePK",
            "calendarDate",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "maxHeartRate",
            "minHeartRate",
            "restingHeartRate",
            "lastSevenDaysAvgRestingHeartRate",
            "heartRateValueDescriptors",
            "heartRateValues",
        }

        if hr["heartRateValues"] is not None:
            for hr_val in hr["heartRateValues"]:
                assert len(hr_val) == 2 and (
                    hr_val[1] is None or 0 < hr_val[1] < 500
                ), (
                    f"HR value is not correct: {hr_val}. "
                    f"Expected a tuple of (timestamp, value) where value is between 0 and 500 or None."
                )
