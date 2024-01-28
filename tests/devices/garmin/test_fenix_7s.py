# perform additional tests specific to the Fenix 7S device

import math
import random
from datetime import datetime, timedelta

import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_fenix_7s(real):
    # first test with default params

    start_synthetic = datetime(2022, 3, 1)
    end_synthetic = datetime(2022, 6, 17)

    device = wearipedia.get_device(
        "garmin/fenix_7s",
        synthetic_start_date=datetime.strftime(start_synthetic, "%Y-%m-%d"),
        synthetic_end_date=datetime.strftime(end_synthetic, "%Y-%m-%d"),
    )

    if real:
        wearipedia._authenticate_device("garmin/fenix_7s", device)

    start_date = "2022-03-01"
    end_date = "2022-06-17"
    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    # HRV
    hrv_data = device.get_hrv_data(start_date, num_days)

    # Verify the length of the HRV data list
    assert len(hrv_data) == num_days, "Number of HRV data entries does not match num_days"

    for entry in hrv_data:
        # Check the structure and data types of the HRV data
        assert isinstance(entry, dict), "Each HRV data entry should be a dictionary"
        expected_keys = {
            "userProfilePk",
            "hrvSummary",
            "hrvReadings",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "sleepStartTimestampGMT",
            "sleepEndTimestampGMT",
            "sleepStartTimestampLocal",
            "sleepEndTimestampLocal",
        }
        assert set(entry.keys()) == expected_keys, "HRV data entry does not have the correct structure"

        # Validate HRV summary values
        hrv_summary = entry['hrvSummary']
        for key in ['calendarDate', 'createTimeStamp']:
            assert isinstance(hrv_summary[key], str), f"{key} should be a string"

        assert isinstance(hrv_summary['lastNightAvg'], int), "lastNightAvg should be an integer"
        assert 15 <= hrv_summary['lastNightAvg'] <= 30, "lastNightAvg is out of expected range"

        assert isinstance(hrv_summary['lastNight5MinHigh'], int), "lastNight5MinHigh should be an integer"
        assert 30 <= hrv_summary['lastNight5MinHigh'] <= 60, "lastNight5MinHigh is out of expected range"

        baseline = hrv_summary['baseline']
        for key in ['lowUpper', 'balancedLow', 'balancedUpper']:
            assert isinstance(baseline[key], int), f"{key} should be an integer"
            assert 15 <= baseline[key] <= 35, f"{key} is out of expected range"

        assert isinstance(baseline['markerValue'], float), "markerValue should be a float"
        assert 0.3 <= baseline['markerValue'] <= 0.6, "markerValue is out of expected range"

        assert hrv_summary['status'] in ['BALANCED', 'ELEVATED', 'LOW'], "Invalid status value"

        # Validate timestamps
        for timestamp_key in ['startTimestampGMT', 'endTimestampGMT', 'startTimestampLocal', 'endTimestampLocal']:
            timestamp = entry[timestamp_key]
            assert isinstance(timestamp, str), f"{timestamp_key} should be a string"
            # Example timestamp format: "2022-03-01T06:00:00.0"
            assert datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.0"), f"{timestamp_key} is not in the correct format"

        # Validate optional sleep timestamps if present
        for sleep_key in ['sleepStartTimestampGMT', 'sleepEndTimestampGMT', 'sleepStartTimestampLocal', 'sleepEndTimestampLocal']:
            if entry[sleep_key] is not None:
                sleep_timestamp = entry[sleep_key]
                assert isinstance(sleep_timestamp, str), f"{sleep_key} should be a string"
                assert datetime.strptime(sleep_timestamp, "%Y-%m-%dT%H:%M:%S.0"), f"{sleep_key} is not in the correct format"

        # Validate HRV readings
        assert isinstance(entry['hrvReadings'], list), "hrvReadings should be a list"

    # Steps
    steps_data = device.get_steps_data(start_date, num_days)

    # Verify the structure of the steps data
    assert isinstance(steps_data, list), "Steps data should be a list"
    assert len(steps_data) == num_days, "Number of entries in steps data should match num_days"

    for daily_steps in steps_data:
        assert isinstance(daily_steps, list), "Each day's steps data should be a list"
        assert len(daily_steps) == 96, "Each day should have 96 intervals of steps data"

        for interval in daily_steps:
            # Check each interval entry structure
            assert set(interval.keys()) == {
                "startGMT", "endGMT", "steps", "pushes", "primaryActivityLevel", "activityLevelConstant"
            }, "Step interval entry does not have the correct structure"

            # Check data types and values
            for time_key in ["startGMT", "endGMT"]:
                assert datetime.strptime(interval[time_key], "%Y-%m-%dT%H:%M:%S.0"), f"Time key {time_key} is not in the correct format"

            assert isinstance(interval['steps'], int), "Steps should be an integer"
            assert 0 <= interval['steps'] <= 200, "Steps value is out of expected range"

            assert isinstance(interval['pushes'], int), "Pushes should be an integer"
            assert interval['pushes'] == 0, "Pushes should always be 0"

            assert interval['primaryActivityLevel'] in ["active", "sedentary", "sleeping", "none"], "Invalid primary activity level"

            assert isinstance(interval['activityLevelConstant'], bool), "Activity level constant indicator should be a boolean"

    # Daily Steps
    daily_steps_data = device.get_daily_steps_data(start_date, num_days)

    # Verify the structure and length of the daily steps data
    assert isinstance(daily_steps_data, list), "Daily steps data should be a list"
    assert len(daily_steps_data) == num_days, "Number of entries in daily steps data should match num_days"

    for day_entry in daily_steps_data:
        assert isinstance(day_entry, list), "Each day's entry should be a list"
        assert len(day_entry) == 1, "Each day's entry should contain exactly one dictionary"

        steps_entry = day_entry[0]
        assert isinstance(steps_entry, dict), "Steps entry should be a dictionary"
        assert set(steps_entry.keys()) == {"calendarDate", "totalSteps", "totalDistance", "stepGoal"}, "Steps entry does not have the correct structure"

        # Check data types and values
        assert datetime.strptime(steps_entry["calendarDate"], "%Y-%m-%d"), "Calendar date is not in the correct format"
        assert isinstance(steps_entry['totalSteps'], int), "Total steps should be an integer"
        assert 5000 <= steps_entry['totalSteps'] <= 20000, "Total steps value is out of expected range"
        assert isinstance(steps_entry['totalDistance'], float), "Total distance should be a float"
        assert isinstance(steps_entry['stepGoal'], int), "Step goal should be an integer"
        assert steps_entry['stepGoal'] == 278, "Step goal value is not as expected"



    # Stats
    stats_data = device.get_stats_data(start_date, num_days)

    # Verify the structure and length of the stats data
    assert isinstance(stats_data, list), "Stats data should be a list"
    assert len(stats_data) == num_days, "Number of entries in stats data should match num_days"

    for entry in stats_data:
        assert isinstance(entry, dict), "Each stats entry should be a dictionary"
        expected_keys = {
            "userProfileId", "totalKilocalories", "activeKilocalories", "bmrKilocalories",
            "wellnessKilocalories", "burnedKilocalories", "consumedKilocalories",
            "remainingKilocalories", "totalSteps", "netCalorieGoal", "totalDistanceMeters",
            "wellnessDistanceMeters", "wellnessActiveKilocalories", "netRemainingKilocalories",
            "userDailySummaryId", "calendarDate", "rule", "uuid", "dailyStepGoal",
            "wellnessStartTimeGmt", "wellnessStartTimeLocal", "wellnessEndTimeGmt",
            "wellnessEndTimeLocal", "durationInMilliseconds", "wellnessDescription",
            "highlyActiveSeconds", "activeSeconds", "sedentarySeconds", "sleepingSeconds",
            "includesWellnessData", "includesActivityData", "includesCalorieConsumedData",
            "privacyProtected", "moderateIntensityMinutes", "vigorousIntensityMinutes",
            "floorsAscendedInMeters", "floorsDescendedInMeters", "floorsAscended",
            "floorsDescended", "intensityMinutesGoal", "userFloorsAscendedGoal", "minHeartRate",
            "maxHeartRate", "restingHeartRate", "lastSevenDaysAvgRestingHeartRate", "source",
            "averageStressLevel", "maxStressLevel", "stressDuration", "restStressDuration",
            "activityStressDuration", "uncategorizedStressDuration", "totalStressDuration",
            "lowStressDuration", "mediumStressDuration", "highStressDuration", "stressPercentage",
            "restStressPercentage", "activityStressPercentage", "uncategorizedStressPercentage",
            "lowStressPercentage", "mediumStressPercentage", "highStressPercentage",
            "stressQualifier", "measurableAwakeDuration", "measurableAsleepDuration",
            "lastSyncTimestampGMT", "minAvgHeartRate", "maxAvgHeartRate", "bodyBatteryChargedValue",
            "bodyBatteryDrainedValue", "bodyBatteryHighestValue", "bodyBatteryLowestValue",
            "bodyBatteryMostRecentValue", "bodyBatteryDuringSleep", "bodyBatteryVersion",
            "abnormalHeartRateAlertsCount", "averageSpo2", "lowestSpo2", "latestSpo2",
            "latestSpo2ReadingTimeGmt", "latestSpo2ReadingTimeLocal", "averageMonitoringEnvironmentAltitude",
            "restingCaloriesFromActivity", "avgWakingRespirationValue", "highestRespirationValue",
            "lowestRespirationValue", "latestRespirationValue", "latestRespirationTimeGMT"
        }
        assert set(entry.keys()) == expected_keys, "Stats entry does not have the correct structure"

        assert isinstance(entry, dict), "Each stats entry should be a dictionary"
        assert isinstance(entry['totalKilocalories'], float), "Total kilocalories should be a float"
        assert 1500 <= entry['totalKilocalories'] <= 3500, "Total kilocalories out of expected range"
        assert isinstance(entry['activeKilocalories'], float), "Active kilocalories should be a float"
        assert 300 <= entry['activeKilocalories'] <= 1000, "Active kilocalories out of expected range"
        assert isinstance(entry['totalSteps'], int), "Total steps should be an integer"
        assert 2000 <= entry['totalSteps'] <= 15000, "Total steps out of expected range"
        assert isinstance(entry['totalDistanceMeters'], float), "Total distance meters should be a float"
        assert 1000 <= entry['totalDistanceMeters'] <= 10000, "Total distance meters out of expected range"
        assert isinstance(entry['dailyStepGoal'], int), "Daily step goal should be an integer"
        assert 3000 <= entry['dailyStepGoal'] <= 10000, "Daily step goal out of expected range"
        assert isinstance(entry['minHeartRate'], int), "Min heart rate should be an integer"
        assert 50 <= entry['minHeartRate'] <= 70, "Min heart rate out of expected range"
        assert isinstance(entry['maxHeartRate'], int), "Max heart rate should be an integer"
        assert 110 <= entry['maxHeartRate'] <= 150, "Max heart rate out of expected range"
        assert isinstance(entry['restingHeartRate'], int), "Resting heart rate should be an integer"
        assert 55 <= entry['restingHeartRate'] <= 75, "Resting heart rate out of expected range"
        assert isinstance(entry['averageStressLevel'], int), "Average stress level should be an integer"
        assert 10 <= entry['averageStressLevel'] <= 50, "Average stress level out of expected range"
        assert isinstance(entry['maxStressLevel'], int), "Max stress level should be an integer"
        assert 50 <= entry['maxStressLevel'] <= 100, "Max stress level out of expected range"
        assert isinstance(entry['stressDuration'], int), "Stress duration should be an integer"
        assert 10000 <= entry['stressDuration'] <= 40000, "Stress duration out of expected range"
        assert isinstance(entry['bodyBatteryHighestValue'], int), "Body battery highest value should be an integer"
        assert 30 <= entry['bodyBatteryHighestValue'] <= 100, "Body battery highest value out of expected range"


    # Body Composition
    body_composition_data = device.get_body_composition_data(start_date, num_days)

    # Verify the structure of the body composition data
    assert isinstance(body_composition_data, dict), "Body composition data should be a dictionary"
    assert 'startDate' in body_composition_data, "Missing startDate in body composition data"
    assert 'endDate' in body_composition_data, "Missing endDate in body composition data"
    assert 'dateWeightList' in body_composition_data, "Missing dateWeightList in body composition data"
    assert 'totalAverage' in body_composition_data, "Missing totalAverage in body composition data"

    # Check startDate and endDate
    assert datetime.strptime(body_composition_data["startDate"], "%Y-%m-%d"), "startDate is not in the correct format"
    assert datetime.strptime(body_composition_data["endDate"], "%Y-%m-%d"), "endDate is not in the correct format"
    assert body_composition_data["endDate"] == (
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days - 1)
    ).strftime("%Y-%m-%d"), "endDate does not match the expected date"

    # Check totalAverage structure
    total_average = body_composition_data['totalAverage']
    assert isinstance(total_average, dict), "totalAverage should be a dictionary"
    expected_keys = {"from", "until", "weight", "bmi", "bodyFat", "bodyWater", "boneMass", "muscleMass", "physiqueRating", "visceralFat", "metabolicAge"}
    assert set(total_average.keys()) == expected_keys, "totalAverage does not have the correct structure"

    # Check timestamps in totalAverage
    assert isinstance(total_average['from'], float), "totalAverage 'from' should be a timestamp"
    assert isinstance(total_average['until'], float), "totalAverage 'until' should be a timestamp"


    # Body Composition Aggregated Data
    body_composition_aggregated_data = device.get_body_composition_aggregated_data(start_date, num_days)

    # Verify the structure and length of the aggregated data
    assert isinstance(body_composition_aggregated_data, list), "Aggregated data should be a list"
    assert len(body_composition_aggregated_data) == num_days, "Number of entries in aggregated data should match num_days"

    for entry in body_composition_aggregated_data:
        assert isinstance(entry, dict), "Each aggregated data entry should be a dictionary"
        assert 'startDate' in entry, "Missing startDate in aggregated data entry"
        assert 'endDate' in entry, "Missing endDate in aggregated data entry"
        assert 'dateWeightList' in entry, "Missing dateWeightList in aggregated data entry"
        assert 'totalAverage' in entry, "Missing totalAverage in aggregated data entry"

        # Check startDate and endDate
        assert datetime.strptime(entry["startDate"], "%Y-%m-%d"), "startDate is not in the correct format"
        assert datetime.strptime(entry["endDate"], "%Y-%m-%d"), "endDate is not in the correct format"
        assert entry["startDate"] == entry["endDate"], "startDate and endDate should be the same in aggregated data"

        # Check totalAverage structure
        total_average = entry['totalAverage']
        assert isinstance(total_average, dict), "totalAverage should be a dictionary"
        expected_keys = {"from", "until", "weight", "bmi", "bodyFat", "bodyWater", "boneMass", "muscleMass", "physiqueRating", "visceralFat", "metabolicAge"}
        assert set(total_average.keys()) == expected_keys, "totalAverage does not have the correct structure"

        # Check timestamps in totalAverage
        assert isinstance(total_average['from'], float), "totalAverage 'from' should be a timestamp"
        assert isinstance(total_average['until'], float), "totalAverage 'until' should be a timestamp"


    # Stats_and_Body Aggregated
    stats_and_body_aggregated_data = device.get_stats_and_body_aggregated_data(start_date, num_days)

    # Verify the structure and length of the aggregated data
    assert isinstance(stats_and_body_aggregated_data, list), "Aggregated data should be a list"
    assert len(stats_and_body_aggregated_data) == num_days, "Number of entries in aggregated data should match num_days"

    for entry in stats_and_body_aggregated_data:
        assert isinstance(entry, dict), "Each aggregated data entry should be a dictionary"
        assert 'stats' in entry and 'body_composition' in entry, "Aggregated data entry should contain 'stats' and 'body_composition' keys"

        # Check 'stats' structure and values
        stats = entry['stats']
        assert isinstance(stats, dict), "'stats' should be a dictionary"
        for key in ['userProfileId', 'totalKilocalories', 'activeKilocalories', 'bmrKilocalories', 'totalSteps', 'totalDistanceMeters']:
            assert key in stats, f"'stats' dictionary should contain the '{key}' key"
            assert isinstance(stats[key], (int, float)), f"'{key}' in 'stats' should be a number"

        # Validate date formats in 'stats'
        for key in ['wellnessStartTimeGmt', 'wellnessEndTimeGmt', 'wellnessStartTimeLocal', 'wellnessEndTimeLocal']:
            assert datetime.strptime(stats[key], "%Y-%m-%dT%H:%M:%S.0"), f"'{key}' in 'stats' should be in correct datetime format"

        # Check 'body_composition' structure and values
        body_composition = entry['body_composition']
        assert isinstance(body_composition, dict), "'body_composition' should be a dictionary"
        for key in ['startDate', 'endDate']:
            assert key in body_composition, f"'body_composition' dictionary should contain the '{key}' key"
            assert datetime.strptime(body_composition[key], "%Y-%m-%d"), f"'{key}' in 'body_composition' should be in correct date format"

        # Check 'totalAverage' structure in 'body_composition'
        total_average = body_composition['totalAverage']
        assert isinstance(total_average, dict), "'totalAverage' in 'body_composition' should be a dictionary"
        for key in ['from', 'until', 'weight', 'bmi', 'bodyFat', 'bodyWater', 'boneMass', 'muscleMass', 'physiqueRating', 'visceralFat', 'metabolicAge']:
            assert key in total_average, f"'totalAverage' dictionary in 'body_composition' should contain the '{key}' key"
            if key in ['from', 'until']:
                assert isinstance(total_average[key], float), f"'{key}' in 'totalAverage' should be a timestamp"
            else:
                assert total_average[key] is None or isinstance(total_average[key], (int, float)), f"'{key}' in 'totalAverage' should be a number or None"

    # Heart Rate
    heart_rate_data = device.get_heart_rate_data(start_date, num_days)

    # Verify the structure and length of the heart rate data
    assert isinstance(heart_rate_data, list), "Heart rate data should be a list"
    assert len(heart_rate_data) == num_days, "Number of entries in heart rate data should match num_days"

    for entry in heart_rate_data:
        assert isinstance(entry, dict), "Each heart rate data entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "startTimestampGMT", "endTimestampGMT",
            "startTimestampLocal", "endTimestampLocal", "maxHeartRate", "minHeartRate",
            "restingHeartRate", "lastSevenDaysAvgRestingHeartRate", "heartRateValueDescriptors", "heartRateValues"
        }
        assert set(entry.keys()) == expected_keys, "Heart rate data entry does not have the correct structure"

        # Check data types and values
        assert datetime.strptime(entry["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "startTimestampGMT is not in the correct format"
        assert datetime.strptime(entry["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "endTimestampGMT is not in the correct format"
        assert isinstance(entry['restingHeartRate'], int), "restingHeartRate should be an integer"
        assert 50 <= entry['restingHeartRate'] <= 90, "restingHeartRate value is out of expected range"
        assert isinstance(entry['maxHeartRate'], int), "maxHeartRate should be an integer"
        assert entry['maxHeartRate'] > entry['restingHeartRate'], "maxHeartRate should be greater than restingHeartRate"
        assert isinstance(entry['minHeartRate'], int), "minHeartRate should be an integer"
        assert entry['minHeartRate'] < entry['maxHeartRate'], "minHeartRate should be less than maxHeartRate"

        # Check heart rate values
        for value in entry['heartRateValues']:
            assert isinstance(value, list) and len(value) == 2, "Each heart rate value entry should be a list of length 2"
            timestamp, heart_rate = value
            assert isinstance(timestamp, int), "Heart rate timestamp should be an integer"
            assert isinstance(heart_rate, int), "Heart rate should be an integer"
            assert entry['minHeartRate'] <= heart_rate <= entry['maxHeartRate'], "Heart rate should be within min and max range"

    # Body Battery
    body_battery_data = device.get_body_battery_data(start_date, num_days)

    # Verify the structure and length of the body battery data
    assert isinstance(body_battery_data, list), "Body battery data should be a list"
    assert len(body_battery_data) == num_days, "Number of entries in body battery data should match num_days"

    for day_entry in body_battery_data:
        assert isinstance(day_entry, list), "Each day's entry should be a list"
        assert len(day_entry) == 1, "Each day's entry should contain exactly one dictionary"

        battery_entry = day_entry[0]
        assert isinstance(battery_entry, dict), "Battery entry should be a dictionary"
        expected_keys = {
            "date", "charged", "drained", "startTimestampGMT", "endTimestampGMT",
            "startTimestampLocal", "endTimestampLocal", "bodyBatteryValuesArray",
            "bodyBatteryValueDescriptorDTOList"
        }
        assert set(battery_entry.keys()) == expected_keys, "Battery entry does not have the correct structure"

        # Check data types and values
        assert datetime.strptime(battery_entry["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "startTimestampGMT is not in the correct format"
        assert datetime.strptime(battery_entry["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "endTimestampGMT is not in the correct format"
        assert isinstance(battery_entry['charged'], int), "Charged value should be an integer"
        assert 0 <= battery_entry['charged'] <= 100, "Charged value should be in the range 0-100"
        assert isinstance(battery_entry['drained'], int), "Drained value should be an integer"
        assert 0 <= battery_entry['drained'] <= 100, "Drained value should be in the range 0-100"

        # Check bodyBatteryValuesArray
        for value_array in battery_entry['bodyBatteryValuesArray']:
            assert isinstance(value_array, list) and len(value_array) == 2, "Each body battery value entry should be a list of length 2"
            timestamp, body_battery_level = value_array
            assert isinstance(timestamp, int), "Timestamp in body battery value should be an integer"
            assert isinstance(body_battery_level, int), "Body battery level should be an integer"
            assert 0 <= body_battery_level <= 100, "Body battery level should be in the range 0-100"


    # Training Readiness
    training_readiness_data = device.get_training_readiness_data(start_date, num_days)

    # Verify the structure and length of the training readiness data
    assert isinstance(training_readiness_data, list), "Training readiness data should be a list"
    assert len(training_readiness_data) == num_days, "Number of entries in training readiness data should match num_days"

    for day_entry in training_readiness_data:
        assert isinstance(day_entry, list), "Each day's entry should be a list"
        assert len(day_entry) == 1, "Each day's entry should contain exactly one dictionary"

        readiness_entry = day_entry[0]
        assert isinstance(readiness_entry, dict), "Readiness entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "timestamp", "timestampLocal", "deviceId",
            "level", "feedbackLong", "feedbackShort", "score", "sleepScore", "sleepScoreFactorPercent",
            "sleepScoreFactorFeedback", "recoveryTime", "recoveryTimeFactorPercent", "recoveryTimeFactorFeedback",
            "acwrFactorPercent", "acwrFactorFeedback", "acuteLoad", "stressHistoryFactorPercent",
            "stressHistoryFactorFeedback", "hrvFactorPercent", "hrvFactorFeedback", "hrvWeeklyAverage",
            "sleepHistoryFactorPercent", "sleepHistoryFactorFeedback", "validSleep", "recoveryTimeChangePhrase"
        }
        assert set(readiness_entry.keys()) == expected_keys, "Readiness entry does not have the correct structure"

        # Check data types and values
        assert datetime.strptime(readiness_entry["timestamp"], "%Y-%m-%dT%H:%M:%S.0"), "timestamp is not in the correct format"
        assert isinstance(readiness_entry['score'], int), "score should be an integer"
        assert 0 <= readiness_entry['score'] <= 100, "score should be in the range 0-100"
        assert isinstance(readiness_entry['sleepScore'], int), "sleepScore should be an integer"
        assert 50 <= readiness_entry['sleepScore'] <= 100, "sleepScore should be in the range 50-100"
        assert isinstance(readiness_entry['recoveryTime'], int), "recoveryTime should be an integer"
        assert 1 <= readiness_entry['recoveryTime'] <= 10, "recoveryTime should be in the range 1-10"
        assert isinstance(readiness_entry['hrvWeeklyAverage'], int), "hrvWeeklyAverage should be an integer"
        assert readiness_entry['hrvWeeklyAverage'] >= 50, "hrvWeeklyAverage should be greater than or equal to 50"


    # Blood Pressure
    blood_pressure_data = device.get_blood_pressure_data(start_date, end_date, num_days)

    # Verify the structure of the blood pressure data
    assert isinstance(blood_pressure_data, dict), "Blood pressure data should be a dictionary"
    expected_keys = {"from", "until", "measurementSummaries", "categoryStats"}
    assert set(blood_pressure_data.keys()) == expected_keys, "Blood pressure data does not have the correct structure"

    # Check data types and values
    assert datetime.strptime(blood_pressure_data["from"], "%Y-%m-%d"), "'from' date is not in the correct format"
    assert datetime.strptime(blood_pressure_data["until"], "%Y-%m-%d"), "'until' date is not in the correct format"
    assert blood_pressure_data["from"] <= blood_pressure_data["until"], "'from' date should be on or before 'until' date"

    # Verify measurementSummaries structure
    measurement_summaries = blood_pressure_data["measurementSummaries"]
    assert isinstance(measurement_summaries, list), "'measurementSummaries' should be a list"

    # Verify the presence of categoryStats
    assert "categoryStats" in blood_pressure_data, "'categoryStats' key should be present in blood pressure data"


    # Floors
    floors_data = device.get_floors_data(start_date, num_days)

    # Verify the structure and length of the floors data
    assert isinstance(floors_data, list), "Floors data should be a list"
    assert len(floors_data) == num_days, "Number of entries in floors data should match num_days"

    for entry in floors_data:
        assert isinstance(entry, dict), "Each floors data entry should be a dictionary"
        expected_keys = {
            "startTimestampGMT", "endTimestampGMT", "startTimestampLocal", "endTimestampLocal",
            "floorsValueDescriptorDTOList", "floorValuesArray"
        }
        assert set(entry.keys()) == expected_keys, "Floors data entry does not have the correct structure"

        # Check timestamps
        assert datetime.strptime(entry["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "startTimestampGMT is not in the correct format"
        assert datetime.strptime(entry["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "endTimestampGMT is not in the correct format"

        # Verify floorValuesArray structure and values
        for floor_value in entry['floorValuesArray']:
            assert isinstance(floor_value, list) and len(floor_value) == 4, "Each floor value entry should be a list of length 4"
            assert datetime.strptime(floor_value[0], "%Y-%m-%dT%H:%M:%S.0"), "Floor value start time is not in the correct format"
            assert datetime.strptime(floor_value[1], "%Y-%m-%dT%H:%M:%S.0"), "Floor value end time is not in the correct format"
            assert isinstance(floor_value[2], int) and 0 <= floor_value[2] <= 10, "Floors ascended should be an integer in range 0-10"
            assert isinstance(floor_value[3], int) and 0 <= floor_value[3] <= 10, "Floors descended should be an integer in range 0-10"

    # Training Status
    training_status_data = device.get_training_status_data(start_date, num_days)

    # Verify the structure and length of the training status data
    assert isinstance(training_status_data, list), "Training status data should be a list"
    assert len(training_status_data) == num_days, "Number of entries in training status data should match num_days"

    for entry in training_status_data:
        assert isinstance(entry, dict), "Each training status data entry should be a dictionary"
        expected_keys = {
            "userId", "mostRecentVO2Max", "mostRecentTrainingLoadBalance",
            "mostRecentTrainingStatus", "heatAltitudeAcclimationDTO"
        }
        assert set(entry.keys()) == expected_keys, "Training status data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userId'], int), "userId should be an integer"


    # Resting Heart Rate
    resting_hr_data = device.get_resting_hr_data(start_date, num_days)

    # Verify the structure of the resting heart rate data
    assert isinstance(resting_hr_data, dict), "Resting heart rate data should be a dictionary"
    expected_keys = {
        "userProfileId", "statisticsStartDate", "statisticsEndDate", "allMetrics", "groupedMetrics"
    }
    assert set(resting_hr_data.keys()) == expected_keys, "Resting heart rate data does not have the correct structure"

    # Check data types and values
    assert isinstance(resting_hr_data['userProfileId'], int), "userProfileId should be an integer"
    assert datetime.strptime(resting_hr_data["statisticsStartDate"], "%Y-%m-%d"), "statisticsStartDate is not in the correct format"
    assert datetime.strptime(resting_hr_data["statisticsEndDate"], "%Y-%m-%d"), "statisticsEndDate is not in the correct format"

    # Verify allMetrics structure and values
    all_metrics = resting_hr_data["allMetrics"]
    assert isinstance(all_metrics, dict), "'allMetrics' should be a dictionary"
    metrics_map = all_metrics.get("metricsMap", {})
    assert "WELLNESS_RESTING_HEART_RATE" in metrics_map, "'metricsMap' should contain 'WELLNESS_RESTING_HEART_RATE'"
    for hr_entry in metrics_map["WELLNESS_RESTING_HEART_RATE"]:
        assert isinstance(hr_entry, dict), "Each resting heart rate entry should be a dictionary"
        assert "value" in hr_entry and "calendarDate" in hr_entry, "Resting heart rate entry should contain 'value' and 'calendarDate'"
        assert isinstance(hr_entry['value'], int), "'value' in resting heart rate entry should be an integer"
        assert 50 <= hr_entry['value'] <= 100, "'value' in resting heart rate entry should be within the range 50-100 bpm"
        assert datetime.strptime(hr_entry["calendarDate"], "%Y-%m-%d"), "'calendarDate' in resting heart rate entry is not in the correct format"


    # Hydration
    hydration_data = device.get_hydration_data(start_date, num_days)

    # Verify the structure and length of the hydration data
    assert isinstance(hydration_data, list), "Hydration data should be a list"
    assert len(hydration_data) == num_days, "Number of entries in hydration data should match num_days"

    for entry in hydration_data:
        assert isinstance(entry, dict), "Each hydration data entry should be a dictionary"
        expected_keys = {
            "userId", "calendarDate", "valueInML", "goalInML", "dailyAverageinML",
            "lastEntryTimestampLocal", "sweatLossInML", "activityIntakeInML"
        }
        assert set(entry.keys()) == expected_keys, "Hydration data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userId'], int), "userId should be an integer"
        assert datetime.strptime(entry["calendarDate"], "%Y-%m-%d"), "calendarDate is not in the correct format"
        # For nullable fields like 'valueInML', checks can be added based on expected behavior
        assert isinstance(entry['goalInML'], float), "goalInML should be a float"
        assert 1800.0 <= entry['goalInML'] <= 2500.0, "goalInML should be in the realistic range of 1800.0-2500.0 ml"


    # Sleep Data
    sleep_data = device.get_sleep_data(start_date, num_days)

    # Verify the structure and length of the sleep data
    assert isinstance(sleep_data, list), "Sleep data should be a list"
    assert len(sleep_data) == num_days, "Number of entries in sleep data should match num_days"

    for entry in sleep_data:
        assert isinstance(entry, dict), "Each sleep data entry should be a dictionary"
        assert "dailySleepDTO" in entry, "Sleep entry should contain 'dailySleepDTO'"
        daily_sleep_dto = entry["dailySleepDTO"]
        expected_keys = {
            "id", "userProfilePK", "calendarDate", "sleepTimeSeconds", "napTimeSeconds",
            "sleepWindowConfirmed", "sleepWindowConfirmationType", "sleepStartTimestampGMT",
            "sleepEndTimestampGMT", "sleepStartTimestampLocal", "sleepEndTimestampLocal",
            "deepSleepSeconds", "lightSleepSeconds", "remSleepSeconds", "awakeSleepSeconds",
            "averageRespirationValue", "lowestRespirationValue", "highestRespirationValue",
            "awakeCount", "avgSleepStress", "ageGroup", "sleepScoreFeedback",
            "sleepScoreInsight", "sleepScores", "sleepVersion"
        }
        assert set(daily_sleep_dto.keys()) == expected_keys, "dailySleepDTO does not have the correct structure"

        # Check data types and values
        assert isinstance(daily_sleep_dto['sleepTimeSeconds'], int), "sleepTimeSeconds should be an integer"
        assert isinstance(daily_sleep_dto['deepSleepSeconds'], int), "deepSleepSeconds should be an integer"
        assert isinstance(daily_sleep_dto['lightSleepSeconds'], int), "lightSleepSeconds should be an integer"
        assert isinstance(daily_sleep_dto['remSleepSeconds'], int), "remSleepSeconds should be an integer"
        assert isinstance(daily_sleep_dto['awakeSleepSeconds'], int), "awakeSleepSeconds should be an integer"

        # Check respiration values
        assert isinstance(daily_sleep_dto['averageRespirationValue'], float), "averageRespirationValue should be a float"
        assert isinstance(daily_sleep_dto['lowestRespirationValue'], float), "lowestRespirationValue should be a float"
        assert isinstance(daily_sleep_dto['highestRespirationValue'], float), "highestRespirationValue should be a float"

        # Verify sleep scores
        assert "sleepScores" in daily_sleep_dto, "dailySleepDTO should contain 'sleepScores'"
        sleep_scores = daily_sleep_dto["sleepScores"]
        for score_key in ["totalDuration", "stress", "awakeCount", "overall", "remPercentage", "lightPercentage", "deepPercentage"]:
            assert score_key in sleep_scores, f"sleepScores should contain '{score_key}'"
            assert isinstance(sleep_scores[score_key]['value'], int), f"The value in '{score_key}' should be an integer"


    # Earned Badge
    earned_badges_data = device.get_earned_badges_data(start_date, num_days)

    # Verify the structure and length of the earned badges data
    assert isinstance(earned_badges_data, list), "Earned badges data should be a list"

    for entry in earned_badges_data:
        assert isinstance(entry, dict), "Each earned badge entry should be a dictionary"
        # Check data types and values
        assert isinstance(entry['badgeId'], int), "badgeId should be an integer"
        assert isinstance(entry['badgeName'], str), "badgeName should be a string"
        assert datetime.strptime(entry["badgeEarnedDate"], "%Y-%m-%dT%H:%M:%S.0"), "badgeEarnedDate is not in the correct format"
        assert isinstance(entry['badgePoints'], int), "badgePoints should be an integer"
        assert 0 <= entry['badgePoints'], "badgePoints should be non-negative"


    # Stress
    stress_data = device.get_stress_data(start_date, num_days)

    # Verify the structure and length of the stress data
    assert isinstance(stress_data, list), "Stress data should be a list"
    assert len(stress_data) == num_days, "Number of entries in stress data should match num_days"

    for entry in stress_data:
        assert isinstance(entry, dict), "Each stress data entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "startTimestampGMT", "endTimestampGMT",
            "startTimestampLocal", "endTimestampLocal", "maxStressLevel", "avgStressLevel",
            "stressChartValueOffset", "stressChartYAxisOrigin", "stressValueDescriptorsDTOList", "stressValuesArray"
        }
        assert set(entry.keys()) == expected_keys, "Stress data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userProfilePK'], int), "userProfilePK should be an integer"
        assert datetime.strptime(entry["calendarDate"], "%Y-%m-%d"), "calendarDate is not in the correct format"
        assert isinstance(entry['maxStressLevel'], int), "maxStressLevel should be an integer"
        assert 70 <= entry['maxStressLevel'] <= 100, "maxStressLevel should be in the range 70-100"
        assert isinstance(entry['avgStressLevel'], int), "avgStressLevel should be an integer"
        assert 20 <= entry['avgStressLevel'] <= 50, "avgStressLevel should be in the range 20-50"

        # Verify stressValuesArray structure and values
        for value in entry['stressValuesArray']:
            assert isinstance(value, list) and len(value) == 2, "Each stress value entry should be a list of length 2"
            timestamp, stress_level = value
            assert isinstance(timestamp, int), "Timestamp in stress value should be an integer"
            assert isinstance(stress_level, int), "Stress level should be an integer"
            assert 10 <= stress_level <= 99, "Stress level should be in the range 10-99"

    # Day Stress Aggregated
    day_stress_aggregated_data = device.get_day_stress_aggregated_data(start_date, num_days)

    # Verify the structure and length of the day stress aggregated data
    assert isinstance(day_stress_aggregated_data, list), "Day stress aggregated data should be a list"
    assert len(day_stress_aggregated_data) == num_days, "Number of entries in day stress aggregated data should match num_days"

    for entry in day_stress_aggregated_data:
        assert isinstance(entry, dict), "Each day stress aggregated data entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "maxStressLevel", "avgStressLevel",
            "stressValueDescriptorsDTOList", "stressValuesArray",
            "bodyBatteryValueDescriptorsDTOList", "bodyBatteryValuesArray"
        }
        assert set(entry.keys()) == expected_keys, "Day stress aggregated data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userProfilePK'], int), "userProfilePK should be an integer"
        assert datetime.strptime(entry["calendarDate"], "%Y-%m-%d"), "calendarDate is not in the correct format"
        assert isinstance(entry['maxStressLevel'], int), "maxStressLevel should be an integer"
        assert isinstance(entry['avgStressLevel'], int), "avgStressLevel should be an integer"

        # Verify stressValuesArray and bodyBatteryValuesArray structure and values
        for stress_value in entry['stressValuesArray']:
            assert isinstance(stress_value, list) and len(stress_value) == 2, "Each stress value entry should be a list of length 2"
            timestamp, stress_level = stress_value
            assert isinstance(timestamp, int), "Timestamp in stress value should be an integer"
            assert isinstance(stress_level, int), "Stress level should be an integer"

        for battery_value in entry['bodyBatteryValuesArray']:
            assert isinstance(battery_value, list) and len(battery_value) == 4, "Each body battery value entry should be a list of length 4"
            timestamp, battery_status, battery_level, version = battery_value
            assert isinstance(timestamp, int), "Timestamp in body battery value should be an integer"
            assert battery_status in ["MEASURED", "ESTIMATED"], "bodyBatteryStatus should be either 'MEASURED' or 'ESTIMATED'"
            assert isinstance(battery_level, int), "bodyBatteryLevel should be an integer"


    # Respiration
    respiration_data = device.get_respiration_data(start_date, num_days)

    # Verify the structure and length of the respiration data
    assert isinstance(respiration_data, list), "Respiration data should be a list"
    assert len(respiration_data) == num_days, "Number of entries in respiration data should match num_days"

    for entry in respiration_data:
        assert isinstance(entry, dict), "Each respiration data entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "startTimestampGMT", "endTimestampGMT",
            "startTimestampLocal", "endTimestampLocal", "sleepStartTimestampGMT",
            "sleepEndTimestampGMT", "sleepStartTimestampLocal", "sleepEndTimestampLocal",
            "tomorrowSleepStartTimestampGMT", "tomorrowSleepEndTimestampGMT",
            "tomorrowSleepStartTimestampLocal", "tomorrowSleepEndTimestampLocal",
            "lowestRespirationValue", "highestRespirationValue",
            "avgWakingRespirationValue", "avgSleepRespirationValue",
            "avgTomorrowSleepRespirationValue", "respirationValueDescriptorsDTOList",
            "respirationValuesArray"
        }
        assert set(entry.keys()) == expected_keys, "Respiration data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userProfilePK'], int), "userProfilePK should be an integer"
        assert datetime.strptime(entry["calendarDate"], "%Y-%m-%d"), "calendarDate is not in the correct format"
        assert isinstance(entry['lowestRespirationValue'], float), "lowestRespirationValue should be a float"
        assert isinstance(entry['highestRespirationValue'], float), "highestRespirationValue should be a float"
        assert isinstance(entry['avgWakingRespirationValue'], float), "avgWakingRespirationValue should be a float"
        assert isinstance(entry['avgSleepRespirationValue'], float), "avgSleepRespirationValue should be a float"
        assert isinstance(entry['avgTomorrowSleepRespirationValue'], float), "avgTomorrowSleepRespirationValue should be a float"

        # Verify respirationValuesArray structure and values
        for value in entry['respirationValuesArray']:
            assert isinstance(value, list) and len(value) == 2, "Each respiration value entry should be a list of length 2"
            timestamp, respiration_value = value
            assert isinstance(timestamp, int), "Timestamp in respiration value should be an integer"
            assert isinstance(respiration_value, float), "Respiration value should be a float"


    # SPO2
    spo2_data = device.get_spo2_data(start_date, num_days)

    # Verify the structure and length of the SpO2 data
    assert isinstance(spo2_data, list), "SpO2 data should be a list"
    assert len(spo2_data) == num_days, "Number of entries in SpO2 data should match num_days"

    for entry in spo2_data:
        assert isinstance(entry, dict), "Each SpO2 data entry should be a dictionary"
        expected_keys = {
            "userProfilePK", "calendarDate", "startTimestampGMT", "endTimestampGMT",
            "startTimestampLocal", "endTimestampLocal", "sleepStartTimestampGMT",
            "sleepEndTimestampGMT", "sleepStartTimestampLocal", "sleepEndTimestampLocal",
            "averageSpO2", "lowestSpO2", "lastSevenDaysAvgSpO2", "latestSpO2",
            "latestSpO2TimestampGMT", "latestSpO2TimestampLocal", "avgSleepSpO2",
            "avgTomorrowSleepSpO2", "spO2ValueDescriptorsDTOList", "spO2SingleValues",
            "continuousReadingDTOList", "spO2HourlyAverages"
        }
        assert set(entry.keys()) == expected_keys, "SpO2 data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['userProfilePK'], int), "userProfilePK should be an integer"
        assert datetime.strptime(entry["calendarDate"], "%Y-%m-%d"), "calendarDate is not in the correct format"

        # Verify timestamps
        assert datetime.strptime(entry["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "startTimestampGMT is not in the correct format"
        assert datetime.strptime(entry["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"), "endTimestampGMT is not in the correct format"


    # Max Metrics
    max_metrics_data = device.get_metrics_data(start_date, num_days)

    # Verify the structure and length of the max metrics data
    assert isinstance(max_metrics_data, list), "Max metrics data should be a list"
    assert len(max_metrics_data) == num_days, "Number of entries in max metrics data should match num_days"

    for entry in max_metrics_data:
        assert isinstance(entry, list), "Each max metrics data entry should be a list"
        assert len(entry) == 1, "Each max metrics data entry should contain one dictionary"
        metrics_entry = entry[0]

        # Check 'generic' data structure and values
        assert "generic" in metrics_entry, "'generic' key should be present in the metrics entry"
        generic_metrics = metrics_entry["generic"]
        assert datetime.strptime(generic_metrics["calendarDate"], "%Y-%m-%d"), "calendarDate in generic metrics is not in the correct format"
        assert isinstance(generic_metrics["vo2MaxPreciseValue"], float), "vo2MaxPreciseValue should be a float"
        assert 30.0 <= generic_metrics["vo2MaxPreciseValue"] <= 50.0, "vo2MaxPreciseValue should be in the range 30.0-50.0"
        assert isinstance(generic_metrics["vo2MaxValue"], int), "vo2MaxValue should be an integer"
        assert 30 <= generic_metrics["vo2MaxValue"] <= 50, "vo2MaxValue should be in the range 30-50"

        # Check 'heatAltitudeAcclimation' data structure and values
        assert "heatAltitudeAcclimation" in metrics_entry, "'heatAltitudeAcclimation' key should be present in the metrics entry"
        acclimation_data = metrics_entry["heatAltitudeAcclimation"]
        assert datetime.strptime(acclimation_data["calendarDate"], "%Y-%m-%d"), "calendarDate in acclimation data is not in the correct format"

    # Personal Records
    personal_record_data = device.get_personal_record_data(start_date, end_date, num_days)

    # Verify the structure and length of the personal record data
    assert isinstance(personal_record_data, list), "Personal record data should be a list"
    assert len(personal_record_data) == num_days, "Number of entries in personal record data should match num_days"

    for entry in personal_record_data:
        assert isinstance(entry, dict), "Each personal record entry should be a dictionary"
        expected_keys = {
            "id", "typeId", "activityId", "activityName", "activityType",
            "activityStartDateTimeInGMT", "actStartDateTimeInGMTFormatted",
            "activityStartDateTimeLocal", "activityStartDateTimeLocalFormatted",
            "value", "prTypeLabelKey", "poolLengthUnit",
            "prStartTimeGmt", "prStartTimeGmtFormatted",
            "prStartTimeLocal", "prStartTimeLocalFormatted"
        }
        assert set(entry.keys()) == expected_keys, "Personal record entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['id'], int), "id should be an integer"
        assert isinstance(entry['typeId'], int), "typeId should be an integer"
        assert isinstance(entry['value'], float), "value should be a float"

        # Verify timestamps
        assert datetime.strptime(entry["prStartTimeGmtFormatted"], "%Y-%m-%dT%H:%M:%S.0"), "prStartTimeGmtFormatted is not in the correct format"
        assert datetime.strptime(entry["prStartTimeLocalFormatted"], "%Y-%m-%dT%H:%M:%S.0"), "prStartTimeLocalFormatted is not in the correct format"


    # Activities
    activities_data = device.get_activities_data(start_date, num_days)

    # Verify the structure and length of the activities data
    assert isinstance(activities_data, list), "Activities data should be a list"
    assert len(activities_data) == num_days, "Number of entries in activities data should match num_days"

    for entry in activities_data:
        assert isinstance(entry, dict), "Each activities data entry should be a dictionary"
        expected_keys = {
            "activityId", "activityName", "description", "startTimeLocal",
            "startTimeGMT", "activityType", "eventType", "comments", "parentId",
            "distance", "duration", "elapsedDuration", "movingDuration",
            "elevationGain", "elevationLoss", "averageSpeed", "maxSpeed",
            "startLatitude", "startLongitude", "hasPolyline", "ownerId",
            "ownerDisplayName", "ownerFullName"
        }
        assert set(entry.keys()) == expected_keys, "Activities data entry does not have the correct structure"

        # Check data types and values
        assert isinstance(entry['activityId'], int), "activityId should be an integer"
        assert datetime.strptime(entry["startTimeLocal"], "%Y-%m-%d %H:%M:%S"), "startTimeLocal is not in the correct format"
        assert datetime.strptime(entry["startTimeGMT"], "%Y-%m-%d %H:%M:%S"), "startTimeGMT is not in the correct format"
        assert isinstance(entry['distance'], float), "distance should be a float"
        assert isinstance(entry['duration'], int), "duration should be an integer"

        # Verify coordinates
        assert -90.0 <= entry['startLatitude'] <= 90.0, "startLatitude should be in the range -90.0 to 90.0"
        assert -180.0 <= entry['startLongitude'] <= 180.0, "startLongitude should be in the range -180.0 to 180.0"

    # Devices
    devices_data = device.get_devices_data(start_date, num_days)

    # Verify the structure of the devices data
    assert isinstance(devices_data, list), "Devices data should be a list"
    expected_num_devices = 3  # As hardcoded in the function
    assert len(devices_data) == expected_num_devices, f"Expected {expected_num_devices} devices data entries"

    for entry in devices_data:
        assert isinstance(entry, dict), "Each devices data entry should be a dictionary"
        # Check data types and values
        assert isinstance(entry['userProfilePk'], int), "userProfilePk should be an integer"
        assert isinstance(entry['unitId'], int), "unitId should be an integer"
        assert isinstance(entry['deviceId'], int), "deviceId should be an integer"
        # Additional checks for other fields

    # Device Last Used
    device_last_used_data = device.get_device_last_used_data("2022-03-01", 10)

    # Verify the structure of the device last used data
    assert isinstance(device_last_used_data, dict), "Device last used data should be a dictionary"

    expected_keys = {
        "userDeviceId", "userProfileNumber", "applicationNumber",
        "lastUsedDeviceApplicationKey", "lastUsedDeviceName",
        "lastUsedDeviceUploadTime", "imageUrl", "released"
    }
    assert set(device_last_used_data.keys()) == expected_keys, "Device last used data does not have the correct structure"

    # Check data types and values
    assert isinstance(device_last_used_data['userDeviceId'], int), "userDeviceId should be an integer"
    assert isinstance(device_last_used_data['userProfileNumber'], int), "userProfileNumber should be an integer"
    assert isinstance(device_last_used_data['applicationNumber'], int), "applicationNumber should be an integer"
    assert isinstance(device_last_used_data['lastUsedDeviceApplicationKey'], str), "lastUsedDeviceApplicationKey should be a string"
    assert isinstance(device_last_used_data['lastUsedDeviceName'], str), "lastUsedDeviceName should be a string"
    assert isinstance(device_last_used_data['released'], bool), "released should be a boolean"


    # Device Settings
    device_settings_data = device.get_device_settings_data(3)

    # Verify the structure and length of the device settings data
    assert isinstance(device_settings_data, list), "Device settings data should be a list"
    assert len(device_settings_data) == 3, "Number of entries in device settings data should match num_devices"

    for entry in device_settings_data:
        assert isinstance(entry, dict), "Each device settings entry should be a dictionary"
        assert isinstance(entry['deviceId'], int), "deviceId should be an integer"
        assert entry['timeFormat'] in ["time_twelve_hr", "time_twenty_four_hr"], "timeFormat should be one of the predefined formats"
        assert isinstance(entry['maxAlarm'], int), "maxAlarm should be an integer"
        assert 0 <= entry['maxAlarm'], "maxAlarm should be non-negative"
        assert isinstance(entry['language'], int), "language should be an integer"
        assert 0 <= entry['language'] < 40, "language should be in the range 0-39"


    # Device Alarms
    device_alarms_data = device.get_device_alarms_data(start_date, num_days)
    assert isinstance(device_alarms_data, list), "Device alarms data should be a list"


    # Active Goals
    active_goals_data = device.get_data("active_goals")
    assert isinstance(active_goals_data, list), "Active goals data should be a list"

    # Future Goals
    future_goals_data = device.get_data("future_goals")
    assert isinstance(future_goals_data, list), "Future goals data should be a list"

    # Past Goals
    past_goals_data = device.get_data("past_goals")
    assert isinstance(past_goals_data, list), "Past goals data should be a list"

    # Weigh-ins
    weigh_ins_data = device.get_weigh_ins_data(start_date, num_days)

    # Verify the structure of the weigh-ins data
    assert isinstance(weigh_ins_data, dict), "Weigh-ins data should be a dictionary"

    expected_keys = {
        "dailyWeightSummaries", "totalAverage", "previousDateWeight", "nextDateWeight"
    }
    assert set(weigh_ins_data.keys()) == expected_keys, "Weigh-ins data does not have the correct structure"

    # Check data types and values
    assert isinstance(weigh_ins_data['totalAverage'], dict), "totalAverage should be a dictionary"
    assert isinstance(weigh_ins_data['previousDateWeight'], dict), "previousDateWeight should be a dictionary"
    assert isinstance(weigh_ins_data['nextDateWeight'], dict), "nextDateWeight should be a dictionary"
    # Verify timestamp formatting and value ranges
    assert weigh_ins_data['totalAverage']['from'] <= weigh_ins_data['totalAverage']['until'], "Timestamp range should be valid"


    # Weigh-ins daily
    weigh_ins_daily_data = device.get_weigh_ins_daily_data(start_date, num_days)

    # Verify the structure and length of the daily weigh-ins data
    assert isinstance(weigh_ins_daily_data, list), "Daily weigh-ins data should be a list"
    assert len(weigh_ins_daily_data) == num_days, "Number of entries in daily weigh-ins data should match num_days"

    for entry in weigh_ins_daily_data:
        assert isinstance(entry, dict), "Each daily weigh-ins entry should be a dictionary"
        expected_keys = {
            "startDate", "endDate", "dateWeightList", "totalAverage"
        }
        assert set(entry.keys()) == expected_keys, "Daily weigh-ins entry does not have the correct structure"

        # Check data types and values
        assert datetime.strptime(entry["startDate"], "%Y-%m-%d"), "startDate should be in the correct format"
        assert datetime.strptime(entry["endDate"], "%Y-%m-%d"), "endDate should be in the correct format"

        # Verify the structure of dateWeightList and totalAverage
        assert isinstance(entry["dateWeightList"], list), "dateWeightList should be a list"
        for weight_entry in entry["dateWeightList"]:
            assert isinstance(weight_entry, dict), "Each weight entry should be a dictionary"
            assert isinstance(weight_entry["weight"], int), "Weight should be an integer"
        assert isinstance(entry["totalAverage"], dict), "totalAverage should be a dictionary"


    # Hill score
    hill_score_data = device.get_hill_score_data(start_date, end_date)

    # Verify the structure of the hill score data
    assert isinstance(hill_score_data, dict), "Hill score data should be a dictionary"

    expected_keys = {
        "userProfilePK", "startDate", "endDate", "periodAvgScore", "maxScore", "hillScoreDTOList"
    }
    assert set(hill_score_data.keys()) == expected_keys, "Hill score data does not have the correct structure"

    assert isinstance(hill_score_data['userProfilePK'], int), "userProfilePK should be an integer"
    assert isinstance(hill_score_data['startDate'], datetime), "startDate should be a datetime object"
    assert isinstance(hill_score_data['endDate'], datetime), "endDate should be a datetime object"
    assert hill_score_data['startDate'] <= hill_score_data['endDate'], "startDate should be before or equal to endDate"

    assert isinstance(hill_score_data['hillScoreDTOList'], list), "hillScoreDTOList should be a list"


    # Endurance Score
    endurance_score_data = device.get_endurance_score_data(start_date, end_date)

    # Verify the structure of the endurance score data
    assert isinstance(endurance_score_data, dict), "Endurance score data should be a dictionary"

    expected_keys = {
        "userProfilePK", "startDate", "endDate", "avg", "max", "groupMap", "enduranceScoreDTO"
    }
    assert set(endurance_score_data.keys()) == expected_keys, "Endurance score data does not have the correct structure"

    # Check data types and values
    assert isinstance(endurance_score_data['userProfilePK'], int), "userProfilePK should be an integer"
    assert isinstance(endurance_score_data['startDate'], datetime), "startDate should be a datetime object"
    assert isinstance(endurance_score_data['endDate'], datetime), "endDate should be a datetime object"
    assert endurance_score_data['startDate'] <= endurance_score_data['endDate'], "startDate should be before or equal to endDate"
    assert isinstance(endurance_score_data['groupMap'], dict), "groupMap should be a dictionary"


    # Adhoc Challenges
    adhoc_challenges_data = device.get_adhoc_challenges_data(start_date, num_days)
    assert isinstance(adhoc_challenges_data, list), "Ad-hoc challenges data should be a list"


    # Available Badges Data
    available_badges_data = device.get_available_badges_data(start_date, num_days)

    # Assertions to check the validity of the generated data
    assert isinstance(available_badges_data, list)

    for entry in available_badges_data:
        # Check the structure and data types of the generated data
        assert isinstance(entry, dict)

        expected_keys = {
            "uuid", "badgeChallengeName", "challengeCategoryId", "badgeChallengeStatusId",
            "startDate", "endDate", "createDate", "updateDate", "badgeId", "badgeKey",
            "badgeUuid", "badgePoints", "badgeUnitId", "badgeProgressValue", "badgeEarnedDate",
            "badgeTargetValue", "badgeTypeIds", "userJoined", "challengeCategoryImageId",
            "badgePromotionCodeTypePk", "badgePromotionCode", "codeExpirationDate",
            "redemptionType", "partnerName", "partnerRewardUrl", "limitedCapacity", "joinDateLocal",
            "challengeGroupPk", "joinable", "approximateValue", "urlEmbeddedSupported"
        }

        assert set(entry.keys()) == expected_keys

        # Check data types for specific fields
        assert isinstance(entry["uuid"], str)
        assert isinstance(entry["badgeChallengeName"], str)
        assert isinstance(entry["challengeCategoryId"], int)
        assert isinstance(entry["badgeChallengeStatusId"], int)
        assert isinstance(entry["startDate"], str) and datetime.strptime(entry["startDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["endDate"], str) and datetime.strptime(entry["endDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["createDate"], str) and datetime.strptime(entry["createDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["updateDate"], str) and datetime.strptime(entry["updateDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["badgeId"], int)
        assert isinstance(entry["badgeKey"], str)
        assert isinstance(entry["badgeUuid"], str)
        assert isinstance(entry["badgePoints"], int)
        assert isinstance(entry["badgeUnitId"], int)
        assert entry["badgeProgressValue"] is None or isinstance(entry["badgeProgressValue"], int)
        assert entry["badgeEarnedDate"] is None or isinstance(entry["badgeEarnedDate"], str)
        assert isinstance(entry["badgeTargetValue"], float)
        assert isinstance(entry["badgeTypeIds"], list) and all(isinstance(val, int) for val in entry["badgeTypeIds"])
        assert isinstance(entry["userJoined"], bool)
        assert isinstance(entry["challengeCategoryImageId"], int)
        assert entry["badgePromotionCodeTypePk"] is None or isinstance(entry["badgePromotionCodeTypePk"], int)
        assert entry["badgePromotionCode"] is None or isinstance(entry["badgePromotionCode"], str)
        assert entry["codeExpirationDate"] is None or isinstance(entry["codeExpirationDate"], str)
        assert entry["redemptionType"] is None or isinstance(entry["redemptionType"], str)
        assert entry["partnerName"] is None or isinstance(entry["partnerName"], str)
        assert entry["partnerRewardUrl"] is None or isinstance(entry["partnerRewardUrl"], str)
        assert isinstance(entry["limitedCapacity"], bool)
        assert entry["joinDateLocal"] is None or isinstance(entry["joinDateLocal"], str)
        assert entry["challengeGroupPk"] is None or isinstance(entry["challengeGroupPk"], int)
        assert isinstance(entry["joinable"], bool)
        assert entry["approximateValue"] is None or isinstance(entry["approximateValue"], str)
        assert isinstance(entry["urlEmbeddedSupported"], bool)

        # Check specific value ranges
        assert 1000 <= entry["badgeId"] <= 2000
        assert 0 <= entry["challengeCategoryId"] <= 10
        assert 1 <= entry["badgeChallengeStatusId"] <= 3
        assert 1 <= entry["badgePoints"] <= 5
        assert 0 <= entry["badgeUnitId"] <= 5
        assert 0.0 <= entry["badgeTargetValue"] <= 10000.0


    # Available Badge Challenges
    available_badge_challenges_data = device.get_available_badge_challenges_data(start_date, num_days)

    # Assertions to check the validity of the generated data
    assert isinstance(available_badge_challenges_data, list)

    for entry in available_badge_challenges_data:
        # Check the structure and data types of the generated data
        assert isinstance(entry, dict)

        expected_keys = {
            "uuid", "badgeChallengeName", "challengeCategoryId", "badgeChallengeStatusId",
            "startDate", "endDate", "createDate", "updateDate", "badgeId", "badgeKey",
            "badgeUuid", "badgePoints", "badgeUnitId", "badgeProgressValue", "badgeEarnedDate",
            "badgeTargetValue", "badgeTypeIds", "userJoined", "challengeCategoryImageId",
            "badgePromotionCodeTypePk", "badgePromotionCode", "codeExpirationDate",
            "redemptionType", "partnerName", "partnerRewardUrl", "limitedCapacity", "joinDateLocal",
            "challengeGroupPk", "joinable", "approximateValue", "urlEmbeddedSupported"
        }

        assert set(entry.keys()) == expected_keys

        # Check data types for specific fields
        assert isinstance(entry["uuid"], str)
        assert isinstance(entry["badgeChallengeName"], str)
        assert isinstance(entry["challengeCategoryId"], int)
        assert isinstance(entry["badgeChallengeStatusId"], int)
        assert isinstance(entry["startDate"], str) and datetime.strptime(entry["startDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["endDate"], str) and datetime.strptime(entry["endDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["createDate"], str) and datetime.strptime(entry["createDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["updateDate"], str) and datetime.strptime(entry["updateDate"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(entry["badgeId"], int)
        assert isinstance(entry["badgeKey"], str)
        assert isinstance(entry["badgeUuid"], str)
        assert isinstance(entry["badgePoints"], int)
        assert isinstance(entry["badgeUnitId"], int)
        assert entry["badgeProgressValue"] is None or isinstance(entry["badgeProgressValue"], int)
        assert entry["badgeEarnedDate"] is None or isinstance(entry["badgeEarnedDate"], str)
        assert isinstance(entry["badgeTargetValue"], float)
        assert isinstance(entry["badgeTypeIds"], list) and all(isinstance(val, int) for val in entry["badgeTypeIds"])
        assert isinstance(entry["userJoined"], bool)
        assert isinstance(entry["challengeCategoryImageId"], int)
        assert entry["badgePromotionCodeTypePk"] is None or isinstance(entry["badgePromotionCodeTypePk"], int)
        assert entry["badgePromotionCode"] is None or isinstance(entry["badgePromotionCode"], str)
        assert entry["codeExpirationDate"] is None or isinstance(entry["codeExpirationDate"], str)
        assert entry["redemptionType"] is None or isinstance(entry["redemptionType"], str)
        assert entry["partnerName"] is None or isinstance(entry["partnerName"], str)
        assert entry["partnerRewardUrl"] is None or isinstance(entry["partnerRewardUrl"], str)
        assert isinstance(entry["limitedCapacity"], bool)
        assert entry["joinDateLocal"] is None or isinstance(entry["joinDateLocal"], str)
        assert entry["challengeGroupPk"] is None or isinstance(entry["challengeGroupPk"], int)
        assert isinstance(entry["joinable"], bool)
        assert entry["approximateValue"] is None or isinstance(entry["approximateValue"], str)
        assert isinstance(entry["urlEmbeddedSupported"], bool)

        # Check specific value ranges
        assert 1000 <= entry["badgeId"] <= 2000
        assert 0 <= entry["challengeCategoryId"] <= 10
        assert 1 <= entry["badgeChallengeStatusId"] <= 3
        assert 1 <= entry["badgePoints"] <= 5
        assert 0 <= entry["badgeUnitId"] <= 10
        assert 0.0 <= entry["badgeTargetValue"] <= 10000.0


    # Activities Date
    activities_date_data = device.get_activities_date_data(start_date, num_days)

    # Assertions to check the validity of the generated data
    assert isinstance(activities_date_data, list)

    for entry in activities_date_data:
        # Check the structure and data types of the generated data
        assert isinstance(entry, dict)

        expected_keys = {
            "activityId", "activityName", "description", "startTimeLocal", "startTimeGMT",
            "activityType", "distance", "duration", "elevationGain", "elevationLoss", "averageSpeed"
        }

        assert set(entry.keys()) == expected_keys

        # Check data types for specific fields
        assert isinstance(entry["activityId"], int)
        assert isinstance(entry["activityName"], str)
        assert entry["description"] is None or isinstance(entry["description"], str)
        assert isinstance(entry["startTimeLocal"], str) and datetime.strptime(entry["startTimeLocal"], "%Y-%m-%d %H:%M:%S")
        assert isinstance(entry["startTimeGMT"], str) and datetime.strptime(entry["startTimeGMT"], "%Y-%m-%d %H:%M:%S")
        assert isinstance(entry["activityType"], dict)
        assert isinstance(entry["distance"], float)
        assert isinstance(entry["duration"], int)
        assert isinstance(entry["elevationGain"], float)
        assert isinstance(entry["elevationLoss"], float)
        assert isinstance(entry["averageSpeed"], float)

        # Check specific value ranges
        assert 100000000 <= entry["activityId"] <= 999999999
        assert 0.0 <= entry["distance"] <= 20.0
        assert 1800 <= entry["duration"] <= 10800
        assert 0.0 <= entry["elevationGain"] <= 500.0
        assert 0.0 <= entry["elevationLoss"] <= 500.0

    # Activities fordate Aggregated
    activities_fordate_aggregated_data = device.get_activities_fordate_aggregated_data(start_date, num_days)

    # Assertions to check the validity of the generated data
    assert isinstance(activities_fordate_aggregated_data, list)

    for entry in activities_fordate_aggregated_data:
        # Check the structure and data types of the generated data
        assert isinstance(entry, dict)

        # Check AllDayHR data
        all_day_hr = entry["AllDayHR"]
        assert isinstance(all_day_hr, dict)
        assert all_day_hr["requestUrl"] == "NA"
        assert all_day_hr["statusCode"] == 200
        assert isinstance(all_day_hr["payload"], dict)

        payload = all_day_hr["payload"]
        assert isinstance(payload["userProfilePK"], int)
        assert isinstance(payload["calendarDate"], str)
        assert isinstance(payload["startTimestampGMT"], str) and datetime.strptime(payload["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(payload["endTimestampGMT"], str) and datetime.strptime(payload["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(payload["startTimestampLocal"], str) and datetime.strptime(payload["startTimestampLocal"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(payload["endTimestampLocal"], str) and datetime.strptime(payload["endTimestampLocal"], "%Y-%m-%dT%H:%M:%S.0")
        assert isinstance(payload["maxHeartRate"], int)
        assert isinstance(payload["minHeartRate"], int)
        assert isinstance(payload["restingHeartRate"], int)
        assert isinstance(payload["lastSevenDaysAvgRestingHeartRate"], int)
        assert isinstance(payload["heartRateValueDescriptors"], list)
        assert all(isinstance(descriptor, dict) for descriptor in payload["heartRateValueDescriptors"])
        assert all("key" in descriptor and "index" in descriptor for descriptor in payload["heartRateValueDescriptors"])
        assert isinstance(payload["heartRateValues"], list)
        assert all(isinstance(value, list) for value in payload["heartRateValues"])
        assert all(len(value) == 2 for value in payload["heartRateValues"])
        assert all(isinstance(value[0], int) and isinstance(value[1], int) for value in payload["heartRateValues"])

        # Check SleepTimes data
        sleep_times = entry["SleepTimes"]
        assert isinstance(sleep_times, dict)
        assert isinstance(sleep_times["currentDaySleepEndTimeGMT"], int)
        assert isinstance(sleep_times["currentDaySleepStartTimeGMT"], int)
        assert isinstance(sleep_times["nextDaySleepEndTimeGMT"], int)
        assert isinstance(sleep_times["nextDaySleepStartTimeGMT"], int)

        # Check ActivitiesForDay data
        activities_for_day = entry["ActivitiesForDay"]
        assert isinstance(activities_for_day, dict)
        assert activities_for_day["requestUrl"] == "NA"
        assert activities_for_day["statusCode"] == 200
        assert isinstance(activities_for_day["payload"], list)
        assert all(isinstance(activity, dict) for activity in activities_for_day["payload"])

    # Badge Challenges
    badge_challenges_data = device.get_badge_challenges_data(start_date, num_days)
    assert isinstance(badge_challenges_data, list)


    # Non Completed Badge Challenges Data
    non_completed_badge_challenges_data = device.get_non_completed_badge_challenges_data(start_date, num_days)
    assert isinstance(non_completed_badge_challenges_data, list)

    # Race Prediction Data
    race_prediction_data = device.get_race_prediction_data(start_date, num_days)
    assert isinstance(race_prediction_data, list)

    # In-progress Virtual Challenges
    inprogress_virtual_challenges_data = device.get_inprogress_virtual_challenges_data(start_date, num_days)
    assert isinstance(inprogress_virtual_challenges_data, list)


