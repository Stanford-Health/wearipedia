# perform additional tests specific to the Fenix 7S device

from datetime import datetime

import wearipedia


def test_fenix_7s_synthetic():
    # first test with default params

    start_synthetic = datetime(2021, 1, 1)
    end_synthetic = datetime(2021, 3, 18)

    device = wearipedia.get_device(
        "garmin/fenix_7s",
        params={
            "synthetic_start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "synthetic_end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )

    dates = device.get_data("dates")
    steps = device.get_data("steps")
    hrs = device.get_data("hrs")
    brpms = device.get_data("brpms")

    assert (
        len(dates)
        == len(steps)
        == len(hrs)
        == len(brpms)
        == (end_synthetic - start_synthetic).days
    ), (
        f"Expected all data to be the same length and to match the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(dates)}, {len(steps)}, "
        f"{len(hrs)}, {len(brpms)}"
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
        for hr_val in hr["heartRateValues"]:
            assert len(hr_val) == 2 and (hr_val[1] is None or 0 < hr_val[1] < 500), (
                f"HR value is not correct: {hr_val}. "
                f"Expected a tuple of (timestamp, value) where value is between 0 and 500 or None."
            )

    # Now make sure that the brpms are correct.
    for brpm in brpms:
        assert set(brpm.keys()) == {
            "userProfilePK",
            "calendarDate",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "sleepStartTimestampGMT",
            "sleepEndTimestampGMT",
            "sleepStartTimestampLocal",
            "sleepEndTimestampLocal",
            "tomorrowSleepStartTimestampGMT",
            "tomorrowSleepEndTimestampGMT",
            "tomorrowSleepStartTimestampLocal",
            "tomorrowSleepEndTimestampLocal",
            "lowestRespirationValue",
            "highestRespirationValue",
            "avgWakingRespirationValue",
            "avgSleepRespirationValue",
            "avgTomorrowSleepRespirationValue",
            "respirationValueDescriptorsDTOList",
            "respirationValuesArray",
        }

        for brpm_val in brpm["respirationValuesArray"]:
            assert len(brpm_val) == 2 and (
                brpm_val[1] is None or 0 < brpm_val[1] < 500
            ), (
                f"BRPM value is not correct: {brpm_val}. "
                f"Expected a tuple of (timestamp, value) where value is between 0 and 500 or None."
            )

    # TODO: stress test with other params
