# perform additional tests specific to the Fenix 7S device

import os
from datetime import datetime

import wearipedia


def test_fenix_7s_real():
    # first test with default params

    device = wearipedia.get_device(
        "garmin/fenix_7s",
    )

    device.authenticate(
        {
            "email": os.environ["GARMIN_FENIX_7S_EMAIL"],
            "password": os.environ["GARMIN_FENIX_7S_PASSWORD"],
        }
    )

    dates = device.get_data("dates")
    steps = device.get_data("steps")
    hrs = device.get_data("hrs")
    brpms = device.get_data("brpms")

    assert len(dates) == len(steps) == len(hrs) == len(brpms), (
        f"Expected all data to be the same length, but got {len(dates)}, {len(steps)}, "
        f"{len(hrs)}, {len(brpms)}"
    )

    # first make sure that the dates are correct
    for date_1, date_2 in zip(dates[:-1], dates[1:]):
        assert (
            date_2 - date_1
        ).days == 1, f"Dates are not consecutive: {date_1}, {date_2}"

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

        # sometimes the heart rate values are missing for some reason
        if hr["heartRateValues"] is not None:
            for hr_val in hr["heartRateValues"]:
                assert len(hr_val) == 2 and (
                    hr_val[1] is None or 0 < hr_val[1] < 500
                ), (
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

        # sometimes the respiration values are missing for some reason
        if brpm["respirationValuesArray"] is not None:
            for brpm_val in brpm["respirationValuesArray"]:
                assert len(brpm_val) == 2 and (
                    brpm_val[1] is None or 0 < brpm_val[1] < 500
                ), (
                    f"BRPM value is not correct: {brpm_val}. "
                    f"Expected a tuple of (timestamp, value) where value is between 0 and 500 or None."
                )

    # TODO: stress test with other params
