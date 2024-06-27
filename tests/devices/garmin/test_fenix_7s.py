# perform additional tests specific to the Fenix 7S device

from datetime import datetime

import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_fenix_7s(real):
    # first test with default params

    start_synthetic = datetime(2021, 1, 1)
    end_synthetic = datetime(2021, 3, 18)

    device = wearipedia.get_device(
        "garmin/fenix_7s",
        synthetic_start_date=datetime.strftime(start_synthetic, "%Y-%m-%d"),
        synthetic_end_date=datetime.strftime(end_synthetic, "%Y-%m-%d"),
    )

    if real:
        wearipedia._authenticate_device("garmin/fenix_7s", device)

    dates = device.get_data("dates")
    steps = device.get_data("steps")
    hr = device.get_data("hr")
    blood_pressure = device.get_data("blood_pressure")
    floors = device.get_data("floors")
    rhr = device.get_data("rhr")
    hydration = device.get_data("hydration")
    sleep = device.get_data("sleep")
    stress = device.get_data("stress")
    respiration = device.get_data("respiration")
    spo2 = device.get_data("spo2")
    hrv = device.get_data("hrv")
    body_battery = device.get_data("body_battery")

    if real:
        # Garmin API has a tendency to rate limit, see
        # https://github.com/cyberjunky/python-garminconnect/issues/85
        # so we just ignore
        return

    assert (
        len(dates) == (end_synthetic - start_synthetic).days
    ), f"Number of days for data generation doesn't match start and end dates: {len(dates)} vs. {(end_synthetic - start_synthetic).days}"

    # first make sure that the dates are correct
    for date_1, date_2 in zip(dates[:-1], dates[1:]):
        assert (
            date_2 - date_1
        ).days == 1, f"Dates are not consecutive: {date_1}, {date_2}"

    assert (
        dates[0] == start_synthetic
    ), f"First date is not correct: {dates[0]} vs. {start_synthetic}"

    # Now make sure that the steps are correct. We're not going overboard with the
    # tests here, but we're just making sure that the data is in the right ballpark.
    for step_day in steps:
        for step in step_day:
            assert set(step.keys()) == {
                "startGMT",
                "endGMT",
                "steps",
                "pushes",
                "primaryActivityLevel",
                "activityLevelConstant",
            }, f"Step data is not correct: generated steps key include {step.keys()}"

    for bb in body_battery:
        assert set(bb[0].keys()) == {
            "date",
            "charged",
            "drained",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "bodyBatteryValuesArray",
            "bodyBatteryValueDescriptorDTOList",
        }, f"Body battery data is not correct: generated data include {bb[0].keys()}"

    for floor in floors:
        assert set(floor.keys()) == {
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "floorsValueDescriptorDTOList",
            "floorValuesArray",
        }, f"Floors data is not correct: {floors.keys()}"

    # Now make sure that the hrs are correct.
    for hr_day in hr:
        assert set(hr_day.keys()) == {
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
        }, f"HR data is not correct: generated HR keys include {hr_day.keys()}"

        if hr_day["heartRateValues"] is not None:
            for hr_val in hr_day["heartRateValues"]:
                assert len(hr_val) == 2 and (
                    hr_val[1] is None or 0 < hr_val[1] < 500
                ), (
                    f"HR value is not correct: {hr_val}. "
                    f"Expected a tuple of (timestamp, value) where value is between 0 and 500 or None."
                )

    assert set(rhr.keys()) == {
        "userProfileId",
        "statisticsStartDate",
        "statisticsEndDate",
        "allMetrics",
        "groupedMetrics",
    }, f"RHR data is not correct: {rhr.keys()}"

    # Check types of some top-level keys
    assert isinstance(
        rhr["userProfileId"], int
    ), f"RHR 'userProfileId' is not an int: {type(rhr['userProfileId'])}"
    assert isinstance(
        datetime.strptime(rhr["statisticsStartDate"], "%Y-%m-%d"), datetime
    ), f"RHR 'statisticsStartDate' is not a valid date: {rhr['statisticsStartDate']}"
    assert isinstance(
        datetime.strptime(rhr["statisticsEndDate"], "%Y-%m-%d"), datetime
    ), f"RHR 'statisticsEndDate' is not a valid date: {rhr['statisticsEndDate']}"

    # Check 'allMetrics' subkeys
    assert set(rhr["allMetrics"].keys()) == {
        "metricsMap"
    }, f"RHR 'allMetrics' keys are not correct: {rhr['allMetrics'].keys()}"

    # Check 'metricsMap' subkeys
    assert set(rhr["allMetrics"]["metricsMap"].keys()) == {
        "WELLNESS_RESTING_HEART_RATE"
    }, f"RHR 'metricsMap' keys are not correct: {rhr['allMetrics']['metricsMap'].keys()}"

    # Check the structure of 'WELLNESS_RESTING_HEART_RATE'
    wrhrs = rhr["allMetrics"]["metricsMap"]["WELLNESS_RESTING_HEART_RATE"]
    assert isinstance(
        wrhrs, list
    ), f"RHR 'WELLNESS_RESTING_HEART_RATE' is not a list: {type(wrhrs)}"

    for wrhr in wrhrs:
        assert (
            "value" in wrhr
        ), f"RHR 'WELLNESS_RESTING_HEART_RATE' entry does not contain 'value': {wrhr}"
        assert isinstance(
            wrhr["value"], int
        ), f"RHR 'WELLNESS_RESTING_HEART_RATE' 'value' is not an int: {type(wrhr['value'])}"

        assert (
            "calendarDate" in wrhr
        ), f"RHR 'WELLNESS_RESTING_HEART_RATE' entry does not contain 'calendarDate': {wrhr}"
        assert isinstance(
            datetime.strptime(wrhr["calendarDate"], "%Y-%m-%d"), datetime
        ), f"RHR 'WELLNESS_RESTING_HEART_RATE' 'calendarDate' is not a valid date: {wrhr['calendarDate']}"

    for hy in hydration:
        assert set(hy.keys()) == {
            "userId",
            "calendarDate",
            "valueInML",
            "goalInML",
            "dailyAverageinML",
            "lastEntryTimestampLocal",
            "sweatLossInML",
            "activityIntakeInML",
        }, f"Hydration data is not correct: {hy.keys()}"

    expected_keys = {
        "dailySleepDTO",
        "sleepMovement",
        "remSleepData",
        "sleepLevels",
        "restingHeartRate",
    }

    daily_sleep_dto_keys = {
        "id",
        "userProfilePK",
        "calendarDate",
        "sleepTimeSeconds",
        "napTimeSeconds",
        "sleepWindowConfirmed",
        "sleepWindowConfirmationType",
        "sleepStartTimestampGMT",
        "sleepEndTimestampGMT",
        "sleepStartTimestampLocal",
        "sleepEndTimestampLocal",
        "autoSleepStartTimestampGMT",
        "autoSleepEndTimestampGMT",
        "sleepQualityTypePK",
        "sleepResultTypePK",
        "unmeasurableSleepSeconds",
        "deepSleepSeconds",
        "lightSleepSeconds",
        "remSleepSeconds",
        "awakeSleepSeconds",
        "deviceRemCapable",
        "retro",
        "sleepFromDevice",
        "averageRespirationValue",
        "lowestRespirationValue",
        "highestRespirationValue",
        "awakeCount",
        "avgSleepStress",
        "ageGroup",
        "sleepScoreFeedback",
        "sleepScoreInsight",
        "sleepScores",
        "sleepVersion",
    }

    sleep_scores_keys = {
        "totalDuration",
        "stress",
        "awakeCount",
        "overall",
        "remPercentage",
        "lightPercentage",
        "deepPercentage",
    }

    for entry in sleep:
        assert (
            set(entry.keys()) == expected_keys
        ), f"Sleep data entry keys are not correct: {entry.keys()}"
        assert (
            set(entry["dailySleepDTO"].keys()) == daily_sleep_dto_keys
        ), f"Sleep data 'dailySleepDTO' keys are not correct: {entry['dailySleepDTO'].keys()}"
        assert (
            set(entry["dailySleepDTO"]["sleepScores"].keys()) == sleep_scores_keys
        ), f"Sleep data 'sleepScores' keys are not correct: {entry['dailySleepDTO']['sleepScores'].keys()}"
