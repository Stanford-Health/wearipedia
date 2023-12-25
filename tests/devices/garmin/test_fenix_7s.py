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
    hrv_data = device.get_data("hrv")
    assert isinstance(hrv_data, list), "HRV data should be a list"
    for entry in hrv_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(hrv_data) == num_days, f"Expected {num_days} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in hrv_data:
        assert set(entry.keys()) == {
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
        }, "Keys in the HRV data entry are not as expected"
        assert isinstance(
            entry["userProfilePk"], int
        ), "UserProfilePk should be an integer"
        assert isinstance(
            entry["hrvSummary"], dict
        ), "hrvSummary should be a dictionary"
        assert isinstance(entry["hrvReadings"], list), "hrvReadings should be a list"

    # Test for Date Consistency
    for i in range(len(hrv_data) - 1):
        current_end = datetime.strptime(
            hrv_data[i]["endTimestampLocal"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        next_start = datetime.strptime(
            hrv_data[i + 1]["startTimestampLocal"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        assert isinstance((next_start - current_end).days, int), "Days are not integer"

    # Test for Valid Range of HRV Metrics
    for entry in hrv_data:
        hrv_summary = entry["hrvSummary"]
        assert 10 <= hrv_summary["lastNightAvg"] <= 40, "Invalid range for lastNightAvg"
        assert (
            30 <= hrv_summary["lastNight5MinHigh"] <= 60
        ), "Invalid range for lastNight5MinHigh"

    # Steps
    steps_data = device.get_data("steps")
    assert isinstance(steps_data, list), "Steps data should be a list"
    for entry in steps_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(steps_data) == num_days, f"Expected {num_days} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in steps_data:
        assert set(entry.keys()) == {
            "userProfilePk",
            "stepsSummary",
            "stepsDetails",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
        }, "Keys in the steps data entry are not as expected"
        assert isinstance(
            entry["userProfilePk"], int
        ), "UserProfilePk should be an integer"
        assert isinstance(
            entry["stepsSummary"], dict
        ), "stepsSummary should be a dictionary"
        assert isinstance(entry["stepsDetails"], list), "stepsDetails should be a list"

    # Test for Date Consistency
    for entry in steps_data:
        for i in range(len(entry["stepsDetails"]) - 1):
            current_end = datetime.strptime(
                entry["stepsDetails"][i]["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"
            )
            next_start = datetime.strptime(
                entry["stepsDetails"][i + 1]["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"
            )
            assert isinstance(
                (next_start - current_end).seconds, int
            ), "Intervals are not valid"

    # Test for Valid Range of Step Counts
    for entry in steps_data:
        steps_summary = entry["stepsSummary"]
        assert (
            1000 <= steps_summary["dailyTotal"] <= 15000
        ), "Invalid range for dailyTotal"
        for step_detail in entry["stepsDetails"]:
            assert 0 <= step_detail["steps"] <= 200, "Invalid range for steps count"

    # Stats
    stats_data = device.get_data("stats")
    assert isinstance(stats_data, list), "Stats data should be a list"
    for entry in stats_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(stats_data) == num_days, f"Expected {num_days} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in stats_data:
        assert isinstance(
            entry["userProfileId"], int
        ), "userProfileId should be an integer"
        assert isinstance(
            entry["totalKilocalories"], float
        ), "totalKilocalories should be a float"
        assert isinstance(
            entry["activeKilocalories"], float
        ), "activeKilocalories should be a float"

    # Test for Date Consistency
    for i in range(len(stats_data)):
        if i < len(stats_data) - 1:
            current_end = datetime.strptime(
                stats_data[i]["wellnessEndTimeGmt"], "%Y-%m-%dT%H:%M:%S.0"
            )
            next_start = datetime.strptime(
                stats_data[i + 1]["wellnessStartTimeGmt"], "%Y-%m-%dT%H:%M:%S.0"
            )
            assert isinstance(
                (next_start - current_end).days, int
            ), "Days are not integer"

    # Test for Valid Range of Metrics (for example: totalKilocalories, totalSteps, etc.)
    for entry in stats_data:
        assert (
            1500.0 <= entry["totalKilocalories"] <= 2500.0
        ), "Invalid range for totalKilocalories"
        assert (
            400.0 <= entry["activeKilocalories"] <= 800.0
        ), "Invalid range for activeKilocalories"

    # Test for valid ranges and relationships among certain metrics
    for entry in stats_data:
        assert (
            entry["remainingKilocalories"] >= 0
            and entry["remainingKilocalories"] <= entry["totalKilocalories"]
        ), "Invalid remainingKilocalories value"

        assert (
            entry["activeKilocalories"] <= entry["totalKilocalories"]
        ), "Active kilocalories exceed total kilocalories"

        assert entry["floorsAscended"] >= 0, "Invalid floors ascended value"
        assert entry["floorsDescended"] >= 0, "Invalid floors descended value"

        assert 50 <= entry["minHeartRate"] <= 70, "Invalid range for minHeartRate"
        assert 120 <= entry["maxHeartRate"] <= 150, "Invalid range for maxHeartRate"
        assert (
            60 <= entry["restingHeartRate"] <= 80
        ), "Invalid range for restingHeartRate"

        assert (
            20.0 <= entry["averageStressLevel"] <= 60.0
        ), "Invalid range for averageStressLevel"
        assert (
            70.0 <= entry["maxStressLevel"] <= 100.0
        ), "Invalid range for maxStressLevel"
        assert (
            10000 <= entry["stressDuration"] <= 40000
        ), "Invalid range for stressDuration"
        assert (
            10.0 <= entry["avgWakingRespirationValue"] <= 20.0
        ), "Invalid range for avgWakingRespirationValue"
        assert (
            15.0 <= entry["highestRespirationValue"] <= 25.0
        ), "Invalid range for highestRespirationValue"
        assert (
            5.0 <= entry["lowestRespirationValue"] <= 15.0
        ), "Invalid range for lowestRespirationValue"
        assert (
            15.0 <= entry["latestRespirationValue"] <= 25.0
        ), "Invalid range for latestRespirationValue"

    # User Summary
    user_summary_data = device.get_data("user_summary")
    assert isinstance(user_summary_data, list), "User summary data should be a list"
    for entry in user_summary_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(user_summary_data) == num_days, f"Expected {num_days} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in user_summary_data:
        assert isinstance(
            entry["userProfileId"], int
        ), "userProfileId should be an integer"
        assert isinstance(
            entry["totalKilocalories"], float
        ), "totalKilocalories should be a float"
        assert isinstance(
            entry["activeKilocalories"], float
        ), "activeKilocalories should be a float"

    # Test for Date Consistency
    for i in range(len(user_summary_data)):
        if i < len(user_summary_data) - 1:
            current_end = datetime.strptime(
                user_summary_data[i]["wellnessEndTimeGmt"], "%Y-%m-%dT%H:%M:%S.0"
            )
            next_start = datetime.strptime(
                user_summary_data[i + 1]["wellnessStartTimeGmt"], "%Y-%m-%dT%H:%M:%S.0"
            )
            assert isinstance(
                (next_start - current_end).days, int
            ), "Days are not integer"

    # Test for Valid Range of Metrics (for example: totalKilocalories, totalSteps, etc.)
    for entry in user_summary_data:
        assert (
            1500.0 <= entry["totalKilocalories"] <= 2500.0
        ), "Invalid range for totalKilocalories"
        assert (
            400.0 <= entry["activeKilocalories"] <= 800.0
        ), "Invalid range for activeKilocalories"

    # Test for valid ranges and relationships among certain metrics
    for entry in user_summary_data:
        assert (
            entry["remainingKilocalories"] >= 0
            and entry["remainingKilocalories"] <= entry["totalKilocalories"]
        ), "Invalid remainingKilocalories value"

        assert (
            entry["activeKilocalories"] <= entry["totalKilocalories"]
        ), "Active kilocalories exceed total kilocalories"

        assert entry["floorsAscended"] >= 0, "Invalid floors ascended value"
        assert entry["floorsDescended"] >= 0, "Invalid floors descended value"

        assert 50 <= entry["minHeartRate"] <= 70, "Invalid range for minHeartRate"
        assert 120 <= entry["maxHeartRate"] <= 150, "Invalid range for maxHeartRate"
        assert (
            60 <= entry["restingHeartRate"] <= 80
        ), "Invalid range for restingHeartRate"

        assert (
            20.0 <= entry["averageStressLevel"] <= 60.0
        ), "Invalid range for averageStressLevel"
        assert (
            70.0 <= entry["maxStressLevel"] <= 100.0
        ), "Invalid range for maxStressLevel"
        assert (
            10000 <= entry["stressDuration"] <= 40000
        ), "Invalid range for stressDuration"
        assert (
            10.0 <= entry["avgWakingRespirationValue"] <= 20.0
        ), "Invalid range for avgWakingRespirationValue"
        assert (
            15.0 <= entry["highestRespirationValue"] <= 25.0
        ), "Invalid range for highestRespirationValue"
        assert (
            5.0 <= entry["lowestRespirationValue"] <= 15.0
        ), "Invalid range for lowestRespirationValue"
        assert (
            15.0 <= entry["latestRespirationValue"] <= 25.0
        ), "Invalid range for latestRespirationValue"

    # Body Composition
    body_comp_data = device.get_data("body_composition")
    assert isinstance(
        body_comp_data, dict
    ), "Body composition data should be a dictionary"
    assert "startDate" in body_comp_data, "Start date should be included in the data"
    assert "endDate" in body_comp_data, "End date should be included in the data"
    assert (
        "dateWeightList" in body_comp_data
    ), "Date weight list should be included in the data"
    assert (
        "totalAverage" in body_comp_data
    ), "Total average metrics should be included in the data"

    # Test for Valid Date Range
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=num_days - 1)
    assert body_comp_data["startDate"] == start_date, "Start date does not match"
    assert body_comp_data["endDate"] == end_date_obj.strftime(
        "%Y-%m-%d"
    ), "End date does not match"

    # Test for Correct Length of Lists
    assert (
        len(body_comp_data["dateWeightList"]) == num_days
    ), "Date weight list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["weight"]) == num_days
    ), "Weight list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["bmi"]) == num_days
    ), "BMI list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["bodyFat"]) == num_days
    ), "Body fat list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["bodyWater"]) == num_days
    ), "Body water list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["boneMass"]) == num_days
    ), "Bone mass list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["muscleMass"]) == num_days
    ), "Muscle mass list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["physiqueRating"]) == num_days
    ), "Physique rating list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["visceralFat"]) == num_days
    ), "Visceral fat list length mismatch"
    assert (
        len(body_comp_data["totalAverage"]["metabolicAge"]) == num_days
    ), "Metabolic age list length mismatch"

    # Test for Valid Values
    for i in range(num_days):
        date = (start_date_obj + timedelta(days=i)).strftime("%Y-%m-%d")

        assert (
            body_comp_data["dateWeightList"][i]["date"] == date
        ), f"Date mismatch at index {i} in dateWeightList"
        assert (
            50 <= body_comp_data["dateWeightList"][i]["weight"] <= 100
        ), f"Invalid weight value at index {i}"

        assert (
            body_comp_data["totalAverage"]["weight"][i]["timestamp"]
            == datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000
        ), f"Timestamp mismatch at index {i} in weight"
        assert (
            50 <= body_comp_data["totalAverage"]["weight"][i]["value"] <= 100
        ), f"Invalid weight value at index {i} in weight"

        assert (
            body_comp_data["totalAverage"]["bmi"][i]["timestamp"]
            == datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000
        ), f"Timestamp mismatch at index {i} in BMI"
        assert (
            18 <= body_comp_data["totalAverage"]["bmi"][i]["value"] <= 30
        ), f"Invalid BMI value at index {i}"

    # Heart Rate Data
    heart_rate_data = device.get_data("hr")
    assert isinstance(heart_rate_data, list), "Heart rate data should be a list"
    for entry in heart_rate_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Valid Data Generation
    for index, entry in enumerate(heart_rate_data):
        assert "userProfilePK" in entry, f"Missing userProfilePK in entry {index}"
        assert "calendarDate" in entry, f"Missing calendarDate in entry {index}"
        assert (
            "startTimestampGMT" in entry
        ), f"Missing startTimestampGMT in entry {index}"
        assert "endTimestampGMT" in entry, f"Missing endTimestampGMT in entry {index}"
        assert (
            "startTimestampLocal" in entry
        ), f"Missing startTimestampLocal in entry {index}"
        assert (
            "endTimestampLocal" in entry
        ), f"Missing endTimestampLocal in entry {index}"
        assert "maxHeartRate" in entry, f"Missing maxHeartRate in entry {index}"
        assert "minHeartRate" in entry, f"Missing minHeartRate in entry {index}"
        assert "restingHeartRate" in entry, f"Missing restingHeartRate in entry {index}"
        assert (
            "lastSevenDaysAvgRestingHeartRate" in entry
        ), f"Missing lastSevenDaysAvgRestingHeartRate in entry {index}"
        assert (
            "heartRateValueDescriptors" in entry
        ), f"Missing heartRateValueDescriptors in entry {index}"
        assert "heartRateValues" in entry, f"Missing heartRateValues in entry {index}"
        assert isinstance(
            entry["userProfilePK"], int
        ), f"userProfilePK should be an integer in entry {index}"
        assert isinstance(
            entry["calendarDate"], str
        ), f"calendarDate should be a string in entry {index}"
        assert isinstance(
            entry["startTimestampGMT"], str
        ), f"startTimestampGMT should be a string in entry {index}"
        assert isinstance(
            entry["endTimestampGMT"], str
        ), f"endTimestampGMT should be a string in entry {index}"
        assert isinstance(
            entry["startTimestampLocal"], str
        ), f"startTimestampLocal should be a string in entry {index}"
        assert isinstance(
            entry["endTimestampLocal"], str
        ), f"endTimestampLocal should be a string in entry {index}"
        assert isinstance(
            entry["maxHeartRate"], int
        ), f"maxHeartRate should be an integer in entry {index}"
        assert isinstance(
            entry["minHeartRate"], int
        ), f"minHeartRate should be an integer in entry {index}"
        assert isinstance(
            entry["restingHeartRate"], int
        ), f"restingHeartRate should be an integer in entry {index}"
        assert isinstance(
            entry["lastSevenDaysAvgRestingHeartRate"], int
        ), f"lastSevenDaysAvgRestingHeartRate should be an integer in entry {index}"
        assert isinstance(
            entry["heartRateValueDescriptors"], list
        ), f"heartRateValueDescriptors should be a list in entry {index}"
        assert isinstance(
            entry["heartRateValues"], list
        ), f"heartRateValues should be a list in entry {index}"
        assert all(
            isinstance(value, str) for value in entry["heartRateValueDescriptors"]
        ), f"All heartRateValueDescriptors should be strings in entry {index}"
        assert all(
            isinstance(value, int) for value in entry["heartRateValues"]
        ), f"All heartRateValues should be integers in entry {index}"

    # Test for Valid Date Range and Calculated Values
    for index, entry in enumerate(heart_rate_data):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(
            days=index
        )
        end_date_obj = start_date_obj + timedelta(days=1)
        assert entry["calendarDate"] == start_date_obj.strftime(
            "%Y-%m-%d"
        ), f"Invalid calendarDate in entry {index}"
        assert (
            entry["startTimestampGMT"]
            == f"{start_date_obj.strftime('%Y-%m-%d')}T07:00:00.0"
        ), f"Invalid startTimestampGMT in entry {index}"
        assert (
            entry["endTimestampGMT"]
            == f"{end_date_obj.strftime('%Y-%m-%d')}T07:00:00.0"
        ), f"Invalid endTimestampGMT in entry {index}"
        assert (
            entry["startTimestampLocal"]
            == f"{start_date_obj.strftime('%Y-%m-%d')}T00:00:00.0"
        ), f"Invalid startTimestampLocal in entry {index}"
        assert (
            entry["endTimestampLocal"]
            == f"{end_date_obj.strftime('%Y-%m-%d')}T00:00:00.0"
        ), f"Invalid endTimestampLocal in entry {index}"
        assert (
            entry["maxHeartRate"] > entry["restingHeartRate"]
        ), f"Max heart rate should be greater than resting heart rate in entry {index}"
        assert (
            entry["minHeartRate"] > entry["restingHeartRate"]
            and entry["minHeartRate"] < entry["maxHeartRate"]
        ), f"Invalid min heart rate in entry {index}"
        assert (
            entry["lastSevenDaysAvgRestingHeartRate"] >= entry["restingHeartRate"] - 2
            and entry["lastSevenDaysAvgRestingHeartRate"]
            <= entry["restingHeartRate"] + 2
        ), f"Invalid last seven days average in entry {index}"

    # Training Readiness
    training_readiness_data = device.get_data("training_readiness")
    assert isinstance(
        training_readiness_data, list
    ), "Training readiness data should be a list"
    for entry in training_readiness_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Valid Data Generation
    for index, entry in enumerate(training_readiness_data):
        assert "userProfilePK" in entry, f"Missing userProfilePK in entry {index}"
        assert "calendarDate" in entry, f"Missing calendarDate in entry {index}"
        assert "timestamp" in entry, f"Missing timestamp in entry {index}"
        assert "timestampLocal" in entry, f"Missing timestampLocal in entry {index}"
        assert "deviceId" in entry, f"Missing deviceId in entry {index}"
        assert "level" in entry, f"Missing level in entry {index}"
        assert "feedbackLong" in entry, f"Missing feedbackLong in entry {index}"
        assert "feedbackShort" in entry, f"Missing feedbackShort in entry {index}"
        assert "sleepScore" in entry, f"Missing sleepScore in entry {index}"
        assert (
            "sleepScoreFactorPercent" in entry
        ), f"Missing sleepScoreFactorPercent in entry {index}"
        assert (
            "sleepScoreFactorFeedback" in entry
        ), f"Missing sleepScoreFactorFeedback in entry {index}"
        assert "recoveryTime" in entry, f"Missing recoveryTime in entry {index}"
        assert (
            "recoveryTimeFactorPercent" in entry
        ), f"Missing recoveryTimeFactorPercent in entry {index}"
        assert (
            "recoveryTimeFactorFeedback" in entry
        ), f"Missing recoveryTimeFactorFeedback in entry {index}"
        assert (
            "acwrFactorPercent" in entry
        ), f"Missing acwrFactorPercent in entry {index}"
        assert (
            "acwrFactorFeedback" in entry
        ), f"Missing acwrFactorFeedback in entry {index}"
        assert "hrvFactorPercent" in entry, f"Missing hrvFactorPercent in entry {index}"
        assert (
            "hrvFactorFeedback" in entry
        ), f"Missing hrvFactorFeedback in entry {index}"
        assert "hrvWeeklyAverage" in entry, f"Missing hrvWeeklyAverage in entry {index}"
        assert (
            "sleepHistoryFactorPercent" in entry
        ), f"Missing sleepHistoryFactorPercent in entry {index}"
        assert (
            "sleepHistoryFactorFeedback" in entry
        ), f"Missing sleepHistoryFactorFeedback in entry {index}"
        assert "validSleep" in entry, f"Missing validSleep in entry {index}"
        assert (
            "recoveryTimeChangePhrase" in entry
        ), f"Missing recoveryTimeChangePhrase in entry {index}"
        assert isinstance(
            entry["userProfilePK"], int
        ), f"userProfilePK should be an integer in entry {index}"
        assert isinstance(
            entry["calendarDate"], str
        ), f"calendarDate should be a string in entry {index}"
        assert isinstance(
            entry["timestamp"], str
        ), f"timestamp should be a string in entry {index}"
        assert isinstance(
            entry["timestampLocal"], str
        ), f"timestampLocal should be a string in entry {index}"
        assert isinstance(
            entry["deviceId"], int
        ), f"deviceId should be an integer in entry {index}"
        assert isinstance(
            entry["level"], str
        ), f"level should be a string in entry {index}"
        assert isinstance(
            entry["feedbackLong"], str
        ), f"feedbackLong should be a string in entry {index}"
        assert isinstance(
            entry["feedbackShort"], str
        ), f"feedbackShort should be a string in entry {index}"
        assert isinstance(
            entry["sleepScore"], int
        ), f"sleepScore should be an integer in entry {index}"
        assert isinstance(
            entry["sleepScoreFactorPercent"], int
        ), f"sleepScoreFactorPercent should be an integer in entry {index}"
        assert isinstance(
            entry["sleepScoreFactorFeedback"], str
        ), f"sleepScoreFactorFeedback should be a string in entry {index}"
        assert isinstance(
            entry["recoveryTime"], int
        ), f"recoveryTime should be an integer in entry {index}"
        assert isinstance(
            entry["recoveryTimeFactorPercent"], int
        ), f"recoveryTimeFactorPercent should be an integer in entry {index}"
        assert isinstance(
            entry["recoveryTimeFactorFeedback"], str
        ), f"recoveryTimeFactorFeedback should be a string in entry {index}"
        assert isinstance(
            entry["acwrFactorPercent"], int
        ), f"acwrFactorPercent should be an integer in entry {index}"
        assert isinstance(
            entry["acwrFactorFeedback"], str
        ), f"acwrFactorFeedback should be a string in entry {index}"
        assert isinstance(
            entry["hrvFactorPercent"], int
        ), f"hrvFactorPercent should be an integer in entry {index}"
        assert isinstance(
            entry["hrvFactorFeedback"], str
        ), f"hrvFactorFeedback should be a string in entry {index}"
        assert isinstance(
            entry["hrvWeeklyAverage"], int
        ), f"hrvWeeklyAverage should be an integer in entry {index}"
        assert isinstance(
            entry["sleepHistoryFactorPercent"], int
        ), f"sleepHistoryFactorPercent should be an integer in entry {index}"
        assert isinstance(
            entry["sleepHistoryFactorFeedback"], str
        ), f"sleepHistoryFactorFeedback should be a string in entry {index}"
        assert isinstance(
            entry["validSleep"], bool
        ), f"validSleep should be a boolean in entry {index}"
        assert entry["recoveryTimeChangePhrase"] is None or isinstance(
            entry["recoveryTimeChangePhrase"], type(None)
        ), f"recoveryTimeChangePhrase should be NoneType or None in entry {index}"

    # Blood Pressure
    num_summaries = num_days
    blood_pressure_data = device.get_data("blood_pressure")
    assert isinstance(
        blood_pressure_data, dict
    ), "Blood pressure data should be a dictionary"
    assert "from" in blood_pressure_data, "Missing 'from' key in blood pressure data"
    assert "until" in blood_pressure_data, "Missing 'until' key in blood pressure data"
    assert (
        "measurementSummaries" in blood_pressure_data
    ), "Missing 'measurementSummaries' key in blood pressure data"
    assert isinstance(
        blood_pressure_data["from"], str
    ), "'from' should be a string in blood pressure data"
    assert isinstance(
        blood_pressure_data["until"], str
    ), "'until' should be a string in blood pressure data"
    assert isinstance(
        blood_pressure_data["measurementSummaries"], list
    ), "'measurementSummaries' should be a list in blood pressure data"

    # Test for Valid Data Generation
    for index, summary in enumerate(blood_pressure_data["measurementSummaries"]):
        assert "date" in summary, f"Missing 'date' key in summary {index}"
        assert "systolic" in summary, f"Missing 'systolic' key in summary {index}"
        assert "diastolic" in summary, f"Missing 'diastolic' key in summary {index}"
        assert "heartRate" in summary, f"Missing 'heartRate' key in summary {index}"
        assert isinstance(
            summary["date"], str
        ), f"'date' should be a string in summary {index}"
        assert isinstance(
            summary["systolic"], int
        ), f"'systolic' should be an integer in summary {index}"
        assert isinstance(
            summary["diastolic"], int
        ), f"'diastolic' should be an integer in summary {index}"
        assert isinstance(
            summary["heartRate"], int
        ), f"'heartRate' should be an integer in summary {index}"
        assert (
            datetime.strptime(blood_pressure_data["from"], "%Y-%m-%d")
            <= datetime.strptime(summary["date"], "%Y-%m-%d")
            <= datetime.strptime(blood_pressure_data["until"], "%Y-%m-%d")
        ), f"'date' in summary {index} should be within the specified range"
        assert (
            90 <= summary["systolic"] <= 160
        ), f"'systolic' in summary {index} should be within the valid range (90-160)"
        assert (
            60 <= summary["diastolic"] <= 100
        ), f"'diastolic' in summary {index} should be within the valid range (60-100)"
        assert (
            60 <= summary["heartRate"] <= 100
        ), f"'heartRate' in summary {index} should be within the valid range (60-100)"

    # Floors
    floors_data = device.get_data("floors")
    assert isinstance(floors_data, list), "Floors data should be a list"
    for data_point in floors_data:
        assert isinstance(data_point, dict), "Each data point should be a dictionary"
        assert "startTimestampGMT" in data_point, "Missing 'startTimestampGMT' key"
        assert "endTimestampGMT" in data_point, "Missing 'endTimestampGMT' key"
        assert "startTimestampLocal" in data_point, "Missing 'startTimestampLocal' key"
        assert "endTimestampLocal" in data_point, "Missing 'endTimestampLocal' key"
        assert "descriptor" in data_point, "Missing 'descriptor' key"
        assert "value" in data_point, "Missing 'value' key"
        assert isinstance(
            data_point["startTimestampGMT"], str
        ), "'startTimestampGMT' should be a string"
        assert isinstance(
            data_point["endTimestampGMT"], str
        ), "'endTimestampGMT' should be a string"
        assert isinstance(
            data_point["startTimestampLocal"], str
        ), "'startTimestampLocal' should be a string"
        assert isinstance(
            data_point["endTimestampLocal"], str
        ), "'endTimestampLocal' should be a string"
        assert isinstance(
            data_point["descriptor"], str
        ), "'descriptor' should be a string"
        assert isinstance(data_point["value"], int), "'value' should be an integer"

    # Training Status
    training_status_data = device.get_data("training_status")
    assert isinstance(
        training_status_data, list
    ), "Training status data should be a list"
    for entry in training_status_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "userId" in entry, "Missing 'userId' key"
        assert "mostRecentVO2Max" in entry, "Missing 'mostRecentVO2Max' key"
        assert (
            "mostRecentTrainingLoadBalance" in entry
        ), "Missing 'mostRecentTrainingLoadBalance' key"
        assert (
            "mostRecentTrainingStatus" in entry
        ), "Missing 'mostRecentTrainingStatus' key"
        assert (
            "heatAltitudeAcclimationDTO" in entry
        ), "Missing 'heatAltitudeAcclimationDTO' key"
        assert isinstance(entry["userId"], int), "'userId' should be an integer"
        assert entry["mostRecentVO2Max"] is None or isinstance(
            entry["mostRecentVO2Max"], (float, int)
        ), "'mostRecentVO2Max' should be None or a number"
        assert entry["mostRecentTrainingLoadBalance"] is None or isinstance(
            entry["mostRecentTrainingLoadBalance"], (float, int)
        ), "'mostRecentTrainingLoadBalance' should be None or a number"
        assert entry["mostRecentTrainingStatus"] is None or isinstance(
            entry["mostRecentTrainingStatus"], str
        ), "'mostRecentTrainingStatus' should be None or a string"
        assert entry["heatAltitudeAcclimationDTO"] is None or isinstance(
            entry["heatAltitudeAcclimationDTO"], dict
        ), "'heatAltitudeAcclimationDTO' should be None or a dictionary"

    # Resting Heart Rate
    resting_hr_data = device.get_data("rhr")

    assert isinstance(
        resting_hr_data, dict
    ), "Resting heart rate data should be a dictionary"
    assert "userProfileId" in resting_hr_data, "Missing 'userProfileId' key"
    assert "statisticsStartDate" in resting_hr_data, "Missing 'statisticsStartDate' key"
    assert "statisticsEndDate" in resting_hr_data, "Missing 'statisticsEndDate' key"
    assert "allMetrics" in resting_hr_data, "Missing 'allMetrics' key"
    assert isinstance(
        resting_hr_data["userProfileId"], int
    ), "'userProfileId' should be an integer"
    assert isinstance(
        resting_hr_data["statisticsStartDate"], str
    ), "'statisticsStartDate' should be a string"
    assert isinstance(
        resting_hr_data["statisticsEndDate"], str
    ), "'statisticsEndDate' should be a string"
    assert isinstance(
        resting_hr_data["allMetrics"], dict
    ), "'allMetrics' should be a dictionary"
    assert "metricsMap" in resting_hr_data["allMetrics"], "Missing 'metricsMap' key"
    assert isinstance(
        resting_hr_data["allMetrics"]["metricsMap"], list
    ), "'metricsMap' should be a list"

    # Test for Date Range and Values
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current_date = start
    index = 0

    while current_date <= end:
        calendar_date = current_date.strftime("%Y-%m-%d")
        assert (
            "WELLNESS_RESTING_HEART_RATE"
            in resting_hr_data["allMetrics"]["metricsMap"][index]
        ), "Missing 'WELLNESS_RESTING_HEART_RATE' key"
        assert isinstance(
            resting_hr_data["allMetrics"]["metricsMap"][index][
                "WELLNESS_RESTING_HEART_RATE"
            ],
            list,
        ), "'WELLNESS_RESTING_HEART_RATE' value should be a list"
        assert (
            len(
                resting_hr_data["allMetrics"]["metricsMap"][index][
                    "WELLNESS_RESTING_HEART_RATE"
                ]
            )
            == 1
        ), "There should be only one metric entry per date"
        metric_entry = resting_hr_data["allMetrics"]["metricsMap"][index][
            "WELLNESS_RESTING_HEART_RATE"
        ][0]
        assert isinstance(metric_entry, dict), "Metric entry should be a dictionary"
        assert "value" in metric_entry, "Missing 'value' key in metric entry"
        assert (
            "calendarDate" in metric_entry
        ), "Missing 'calendarDate' key in metric entry"
        assert isinstance(
            metric_entry["value"], float
        ), "'value' should be a floating-point number"
        assert isinstance(
            metric_entry["calendarDate"], str
        ), "'calendarDate' should be a string"
        assert (
            metric_entry["calendarDate"] == calendar_date
        ), f"Date mismatch: {metric_entry['calendarDate']} != {calendar_date}"
        current_date += timedelta(days=1)
        index += 1

    # Hydration
    hydration_data = device.get_data("hydration")

    assert isinstance(hydration_data, list), "Hydration data should be a list"
    assert len(hydration_data) == num_days, f"Expected {num_days} days of data"

    # Test for Data Structure and Types
    for entry in hydration_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "userId" in entry, "Missing 'userId' key"
        assert isinstance(entry["userId"], int), "'userId' should be an integer"
        assert "calendarDate" in entry, "Missing 'calendarDate' key"
        assert isinstance(
            entry["calendarDate"], str
        ), "'calendarDate' should be a string"
        assert "valueInML" in entry, "Missing 'valueInML' key"
        assert entry["valueInML"] is None or isinstance(
            entry["valueInML"], float
        ), "'valueInML' should be a float or None"
        assert "goalInML" in entry, "Missing 'goalInML' key"
        assert isinstance(entry["goalInML"], float), "'goalInML' should be a float"
        assert "dailyAverageinML" in entry, "Missing 'dailyAverageinML' key"
        assert entry["dailyAverageinML"] is None or isinstance(
            entry["dailyAverageinML"], float
        ), "'dailyAverageinML' should be a float or None"
        assert (
            "lastEntryTimestampLocal" in entry
        ), "Missing 'lastEntryTimestampLocal' key"
        assert entry["lastEntryTimestampLocal"] is None or isinstance(
            entry["lastEntryTimestampLocal"], str
        ), "'lastEntryTimestampLocal' should be a string or None"
        assert "sweatLossInML" in entry, "Missing 'sweatLossInML' key"
        assert entry["sweatLossInML"] is None or isinstance(
            entry["sweatLossInML"], float
        ), "'sweatLossInML' should be a float or None"
        assert "activityIntakeInML" in entry, "Missing 'activityIntakeInML' key"
        assert entry["activityIntakeInML"] is None or isinstance(
            entry["activityIntakeInML"], float
        ), "'activityIntakeInML' should be a float or None"

    # Sleep Data
    sleep_data = device.get_data("sleep")

    assert isinstance(sleep_data, list), "Sleep data should be a list"
    assert len(sleep_data) == num_days, f"Expected {num_days} days of sleep data"

    # Test for Data Structure and Types
    for entry in sleep_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "dailySleepDTO" in entry, "Missing 'dailySleepDTO' key"
        daily_sleep_dto = entry["dailySleepDTO"]
        assert isinstance(
            daily_sleep_dto, dict
        ), "'dailySleepDTO' should be a dictionary"
        assert "id" in daily_sleep_dto, "Missing 'id' key"
        assert isinstance(daily_sleep_dto["id"], int), "'id' should be an integer"
        assert "userProfilePK" in daily_sleep_dto, "Missing 'userProfilePK' key"
        assert isinstance(
            daily_sleep_dto["userProfilePK"], int
        ), "'userProfilePK' should be an integer"
        assert "calendarDate" in daily_sleep_dto, "Missing 'calendarDate' key"
        assert isinstance(
            daily_sleep_dto["calendarDate"], str
        ), "'calendarDate' should be a string"

    # Earned Badge
    earned_badges_data = device.get_data("earned_badges")

    assert isinstance(earned_badges_data, list), "Earned badges data should be a list"

    # Test for Data Structure and Types
    for entry in earned_badges_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "badgeId" in entry, "Missing 'badgeId' key"
        assert isinstance(entry["badgeId"], int), "'badgeId' should be an integer"
        assert "badgeCategory" in entry, "Missing 'badgeCategory' key"
        assert isinstance(
            entry["badgeCategory"], str
        ), "'badgeCategory' should be a string"
        assert "badgeName" in entry, "Missing 'badgeName' key"
        assert isinstance(entry["badgeName"], str), "'badgeName' should be a string"
        assert "badgeEarnedDate" in entry, "Missing 'badgeEarnedDate' key"
        assert isinstance(
            entry["badgeEarnedDate"], str
        ), "'badgeEarnedDate' should be a string"

    # Stress
    stress_data = device.get_data("stress")

    assert isinstance(stress_data, list), "Stress data should be a list"

    # Test for Data Structure and Types
    for entry in stress_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "userProfilePK" in entry, "Missing 'userProfilePK' key"
        assert isinstance(
            entry["userProfilePK"], int
        ), "'userProfilePK' should be an integer"
        assert "calendarDate" in entry, "Missing 'calendarDate' key"
        assert isinstance(
            entry["calendarDate"], str
        ), "'calendarDate' should be a string"
        assert "startTimestampGMT" in entry, "Missing 'startTimestampGMT' key"
        assert isinstance(
            entry["startTimestampGMT"], str
        ), "'startTimestampGMT' should be a string"
        assert "endTimestampGMT" in entry, "Missing 'endTimestampGMT' key"
        assert isinstance(
            entry["endTimestampGMT"], str
        ), "'endTimestampGMT' should be a string"
        assert "startTimestampLocal" in entry, "Missing 'startTimestampLocal' key"
        assert isinstance(
            entry["startTimestampLocal"], str
        ), "'startTimestampLocal' should be a string"
        assert "endTimestampLocal" in entry, "Missing 'endTimestampLocal' key"
        assert isinstance(
            entry["endTimestampLocal"], str
        ), "'endTimestampLocal' should be a string"

        assert "maxStressLevel" in entry, "Missing 'maxStressLevel' key"
        assert isinstance(
            entry["maxStressLevel"], int
        ), "'maxStressLevel' should be an integer"
        assert (
            70 <= entry["maxStressLevel"] <= 100
        ), "'maxStressLevel' should be between 70 and 100"

        assert "avgStressLevel" in entry, "Missing 'avgStressLevel' key"
        assert isinstance(
            entry["avgStressLevel"], int
        ), "'avgStressLevel' should be an integer"
        assert (
            20 <= entry["avgStressLevel"] <= 50
        ), "'avgStressLevel' should be between 20 and 50"

    # Respiration
    respiration_data = device.get_data("respiration")

    assert isinstance(respiration_data, list), "Respiration data should be a list"

    # Test for Data Structure and Types
    for entry in respiration_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "userProfilePK" in entry, "Missing 'userProfilePK' key"
        assert isinstance(
            entry["userProfilePK"], int
        ), "'userProfilePK' should be an integer"
        assert "calendarDate" in entry, "Missing 'calendarDate' key"
        assert isinstance(
            entry["calendarDate"], str
        ), "'calendarDate' should be a string"
        assert "startTimestampGMT" in entry, "Missing 'startTimestampGMT' key"
        assert isinstance(
            entry["startTimestampGMT"], str
        ), "'startTimestampGMT' should be a string"
        assert "endTimestampGMT" in entry, "Missing 'endTimestampGMT' key"
        assert isinstance(
            entry["endTimestampGMT"], str
        ), "'endTimestampGMT' should be a string"
        assert "startTimestampLocal" in entry, "Missing 'startTimestampLocal' key"
        assert isinstance(
            entry["startTimestampLocal"], str
        ), "'startTimestampLocal' should be a string"
        assert "endTimestampLocal" in entry, "Missing 'endTimestampLocal' key"
        assert isinstance(
            entry["endTimestampLocal"], str
        ), "'endTimestampLocal' should be a string"

        assert "lowestRespirationValue" in entry, "Missing 'lowestRespirationValue' key"
        assert isinstance(
            entry["lowestRespirationValue"], float
        ), "'lowestRespirationValue' should be a float"
        assert (
            10.0 <= entry["lowestRespirationValue"] <= 15.0
        ), "'lowestRespirationValue' should be between 10.0 and 15.0"

        assert (
            "highestRespirationValue" in entry
        ), "Missing 'highestRespirationValue' key"
        assert isinstance(
            entry["highestRespirationValue"], float
        ), "'highestRespirationValue' should be a float"
        assert (
            20.0 <= entry["highestRespirationValue"] <= 25.0
        ), "'highestRespirationValue' should be between 20.0 and 25.0"

        assert (
            "avgWakingRespirationValue" in entry
        ), "Missing 'avgWakingRespirationValue' key"
        assert isinstance(
            entry["avgWakingRespirationValue"], float
        ), "'avgWakingRespirationValue' should be a float"
        assert "sleepStartTimestampGMT" in entry, "Missing 'sleepStartTimestampGMT' key"
        assert isinstance(
            entry["sleepStartTimestampGMT"], str
        ), "'sleepStartTimestampGMT' should be a string"

    # SPO2
    spo2_data = device.get_data("spo2")

    assert isinstance(spo2_data, list), "SpO2 data should be a list"

    # Test for Data Structure and Types
    for entry in spo2_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"
        assert "userProfilePK" in entry, "Missing 'userProfilePK' key"
        assert isinstance(
            entry["userProfilePK"], int
        ), "'userProfilePK' should be an integer"
        assert "calendarDate" in entry, "Missing 'calendarDate' key"
        assert isinstance(
            entry["calendarDate"], str
        ), "'calendarDate' should be a string"
        assert "startTimestampGMT" in entry, "Missing 'startTimestampGMT' key"
        assert isinstance(
            entry["startTimestampGMT"], str
        ), "'startTimestampGMT' should be a string"
        assert "averageSpO2" in entry, "Missing 'averageSpO2' key"
        assert isinstance(
            entry["averageSpO2"], float
        ), "'averageSpO2' should be a float"
        assert (
            92.0 <= entry["averageSpO2"] <= 99.0
        ), "'averageSpO2' should be between 92.0 and 99.0"

        assert "lowestSpO2" in entry, "Missing 'lowestSpO2' key"
        assert isinstance(entry["lowestSpO2"], float), "'lowestSpO2' should be a float"
        assert (
            88.0 <= entry["lowestSpO2"] <= 91.0
        ), "'lowestSpO2' should be between 88.0 and 91.0"

        assert "lastSevenDaysAvgSpO2" in entry, "Missing 'lastSevenDaysAvgSpO2' key"
        assert isinstance(
            entry["lastSevenDaysAvgSpO2"], float
        ), "'lastSevenDaysAvgSpO2' should be a float"

    # Max Metrics
    metrics_data = device.get_data("max_metrics")

    assert isinstance(metrics_data, list), "Metrics data should be a list"

    # Validate Each Entry in the List
    for entry in metrics_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

        assert "userId" in entry and isinstance(
            entry["userId"], int
        ), "Invalid or missing 'userId' value"

        assert "generic" in entry and isinstance(
            entry["generic"], dict
        ), "Invalid or missing 'generic' key"
        generic_metrics = entry["generic"]
        assert "calendarDate" in generic_metrics and isinstance(
            generic_metrics["calendarDate"], str
        ), "Invalid or missing 'calendarDate' value"
        assert "vo2MaxPreciseValue" in generic_metrics and isinstance(
            generic_metrics["vo2MaxPreciseValue"], float
        ), "Invalid or missing 'vo2MaxPreciseValue' value"
        assert "vo2MaxValue" in generic_metrics and isinstance(
            generic_metrics["vo2MaxValue"], float
        ), "Invalid or missing 'vo2MaxValue' value"
        assert (
            35.0 <= generic_metrics["vo2MaxPreciseValue"] <= 41.0
        ), "vo2MaxPreciseValue out of range"
        assert (
            35.0 <= generic_metrics["vo2MaxValue"] <= 41.0
        ), "vo2MaxValue out of range"

    # Personal Records
    num_entries = num_days
    pr_data = device.get_data("personal_record")
    assert isinstance(pr_data, list), "Personal record data should be a list"
    for entry in pr_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(pr_data) == num_entries, f"Expected {num_entries} entries of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in pr_data:
        expected_keys = [
            "id",
            "typeId",
            "activityId",
            "activityName",
            "activityType",
            "activityStartDateTimeInGMT",
            "actStartDateTimeInGMTFormatted",
            "activityStartDateTimeLocal",
            "activityStartDateTimeLocalFormatted",
            "value",
            "prTypeLabelKey",
            "poolLengthUnit",
            "prStartTimeGmt",
            "prStartTimeGmtFormatted",
            "prStartTimeLocal",
            "prStartTimeLocalFormatted",
        ]
        assert set(entry.keys()) == set(
            expected_keys
        ), "Keys in the personal record data entry are not as expected"
        assert isinstance(entry["id"], int), "ID should be an integer"
        assert isinstance(entry["typeId"], int), "TypeID should be an integer"
        assert isinstance(entry["activityId"], int), "ActivityID should be an integer"
        assert entry["activityName"] is None or isinstance(
            entry["activityName"], str
        ), "ActivityName should be a string or None"
        assert entry["activityType"] is None or isinstance(
            entry["activityType"], str
        ), "ActivityType should be a string or None"
        assert entry["activityStartDateTimeInGMT"] is None or isinstance(
            entry["activityStartDateTimeInGMT"], str
        ), "ActivityStartDateTimeInGMT should be a string or None"

    # Test for Date Consistency
    for i in range(len(pr_data)):
        if i < len(pr_data) - 1:
            current_end = datetime.strptime(
                pr_data[i]["prStartTimeGmtFormatted"], "%Y-%m-%dT%H:%M:%S.0"
            )
            next_start = datetime.strptime(
                pr_data[i + 1]["prStartTimeGmtFormatted"], "%Y-%m-%dT%H:%M:%S.0"
            )
            assert isinstance(
                (next_start - current_end).days, int
            ), "Days are not integer"

    # Activities
    activities_data = device.get_data("activities")
    assert isinstance(activities_data, list), "Activities data should be a list"
    for entry in activities_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    assert len(activities_data) == num_days, f"Expected {num_days} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in activities_data:
        expected_keys = [
            "userProfilePK",
            "calendarDate",
            "startTimestampGMT",
            "endTimestampGMT",
            "startTimestampLocal",
            "endTimestampLocal",
            "activityType",
            "durationMinutes",
            "caloriesBurned",
        ]
        assert set(entry.keys()) == set(
            expected_keys
        ), "Keys in the activities data entry are not as expected"
        assert isinstance(
            entry["userProfilePK"], int
        ), "userProfilePK should be an integer"
        assert isinstance(entry["calendarDate"], str), "calendarDate should be a string"
        assert isinstance(
            entry["startTimestampGMT"], str
        ), "startTimestampGMT should be a string"

    # Test for Date Consistency
    for entry in activities_data:
        start_timestamp_gmt = datetime.strptime(
            entry["startTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"
        )
        end_timestamp_gmt = datetime.strptime(
            entry["endTimestampGMT"], "%Y-%m-%dT%H:%M:%S.0"
        )
        start_timestamp_local = datetime.strptime(
            entry["startTimestampLocal"], "%Y-%m-%dT%H:%M:%S.0"
        )
        end_timestamp_local = datetime.strptime(
            entry["endTimestampLocal"], "%Y-%m-%dT%H:%M:%S.0"
        )

        assert (
            end_timestamp_gmt - start_timestamp_gmt
        ).days == 1, "Dates are not consecutive"
        assert (
            end_timestamp_local - start_timestamp_local
        ).days == 1, "Local Dates are not consecutive"

    for entry in activities_data:
        assert (
            15 <= entry["durationMinutes"] <= 120
        ), "Invalid range for durationMinutes"
        assert 100 <= entry["caloriesBurned"] <= 600, "Invalid range for caloriesBurned"

    # Active Goals
    active_goals_data = device.get_data("active_goals")
    assert isinstance(active_goals_data, list), "Active goals data should be a list"
    for entry in active_goals_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    expected_length = num_days
    assert (
        len(active_goals_data) == expected_length + 1
    ), f"Expected {expected_length} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in active_goals_data:
        expected_keys = ["goalType", "goalValue", "startDate", "endDate"]
        assert set(entry.keys()) == set(
            expected_keys
        ), "Keys in the active goals data entry are not as expected"
        assert isinstance(entry["goalType"], str), "goalType should be a string"
        assert entry["goalType"] in [
            "step",
            "distance",
            "calories",
            "activeMinutes",
        ], "Invalid goalType"
        assert isinstance(entry["goalValue"], int), "goalValue should be an integer"
        assert isinstance(
            entry["startDate"], datetime
        ), "startDate should be a datetime object"
        assert isinstance(
            entry["endDate"], datetime
        ), "endDate should be a datetime object"

    # Test for Date Consistency and Range
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    for entry in active_goals_data:
        assert entry["startDate"] == current_date, "Start date mismatch"
        assert entry["endDate"] == current_date, "End date mismatch"
        current_date += timedelta(days=1)

    # Future Goals
    future_goals_data = device.get_data("future_goals")
    assert isinstance(future_goals_data, list), "Future goals data should be a list"
    for entry in future_goals_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    expected_length = num_days
    assert (
        len(future_goals_data) == expected_length + 1
    ), f"Expected {expected_length} days of data"

    for entry in future_goals_data:
        expected_keys = ["goalType", "goalValue", "startDate", "endDate"]
        assert set(entry.keys()) == set(
            expected_keys
        ), "Keys in the future goals data entry are not as expected"
        assert isinstance(entry["goalType"], str), "goalType should be a string"
        assert entry["goalType"] in [
            "step",
            "distance",
            "calories",
            "activeMinutes",
        ], "Invalid goalType"
        assert isinstance(entry["goalValue"], int), "goalValue should be an integer"
        assert isinstance(
            entry["startDate"], datetime
        ), "startDate should be a datetime object"
        assert isinstance(
            entry["endDate"], datetime
        ), "endDate should be a datetime object"

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    for entry in future_goals_data:
        assert entry["startDate"] == current_date, "Start date mismatch"
        assert entry["endDate"] == current_date, "End date mismatch"
        current_date += timedelta(days=1)

    # Past Goals
    past_goals_data = device.get_data("past_goals")
    assert isinstance(past_goals_data, list), "Past goals data should be a list"
    for entry in past_goals_data:
        assert isinstance(entry, dict), "Each entry should be a dictionary"

    # Test for Correct Data Length
    expected_length = num_days
    assert (
        len(past_goals_data) == expected_length + 1
    ), f"Expected {expected_length} days of data"

    # Test for Valid Keys and Types in Each Dictionary
    for entry in past_goals_data:
        expected_keys = ["goalType", "goalValue", "startDate", "endDate"]
        assert set(entry.keys()) == set(
            expected_keys
        ), "Keys in the past goals data entry are not as expected"
        assert isinstance(entry["goalType"], str), "goalType should be a string"
        assert entry["goalType"] in [
            "step",
            "distance",
            "calories",
            "activeMinutes",
        ], "Invalid goalType"
        assert isinstance(entry["goalValue"], int), "goalValue should be an integer"
        assert isinstance(
            entry["startDate"], datetime
        ), "startDate should be a datetime object"
        assert isinstance(
            entry["endDate"], datetime
        ), "endDate should be a datetime object"

    # Test for Date Consistency and Range
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    for entry in past_goals_data:
        assert entry["startDate"] == current_date, "Start date mismatch"
        assert entry["endDate"] == current_date, "End date mismatch"
        current_date += timedelta(days=1)

    # Weigh-ins
    weigh_ins_data = device.get_data("weigh_ins")

    # Check total average values for reasonable ranges
    assert (
        60 <= weigh_ins_data["totalAverage"]["weight"] <= 90
    ), "Invalid range for weight in total average"
    assert (
        18 <= weigh_ins_data["totalAverage"]["bmi"] <= 30
    ), "Invalid range for BMI in total average"
    assert (
        10 <= weigh_ins_data["totalAverage"]["bodyFat"] <= 25
    ), "Invalid range for body fat in total average"
    assert (
        45 <= weigh_ins_data["totalAverage"]["bodyWater"] <= 65
    ), "Invalid range for body water in total average"
    assert (
        2 <= weigh_ins_data["totalAverage"]["boneMass"] <= 5
    ), "Invalid range for bone mass in total average"
    assert (
        30 <= weigh_ins_data["totalAverage"]["muscleMass"] <= 60
    ), "Invalid range for muscle mass in total average"
    assert weigh_ins_data["totalAverage"]["physiqueRating"] in [
        "Good",
        "Average",
        "Excellent",
    ], "Invalid physique rating in total average"
    assert (
        5 <= weigh_ins_data["totalAverage"]["visceralFat"] <= 15
    ), "Invalid range for visceral fat in total average"
    assert (
        20 <= weigh_ins_data["totalAverage"]["metabolicAge"] <= 60
    ), "Invalid range for metabolic age in total average"

    assert (
        58 <= weigh_ins_data["previousDateWeight"]["weight"] <= 92
    ), "Invalid range for previous date weight"
    assert (
        58 <= weigh_ins_data["nextDateWeight"]["weight"] <= 92
    ), "Invalid range for next date weight"

    for summary in weigh_ins_data["dailyWeightSummaries"]:
        assert 59 <= summary["weight"] <= 91, "Invalid range for daily weight summaries"

    # Weigh-ins daily
    weigh_ins_daily_data = device.get_data("weigh_ins_daily")

    assert (
        60 <= weigh_ins_daily_data["totalAverage"]["weight"] <= 90
    ), "Invalid range for weight in total average"
    assert (
        18 <= weigh_ins_daily_data["totalAverage"]["bmi"] <= 30
    ), "Invalid range for BMI in total average"
    assert (
        10 <= weigh_ins_daily_data["totalAverage"]["bodyFat"] <= 25
    ), "Invalid range for body fat in total average"
    assert (
        45 <= weigh_ins_daily_data["totalAverage"]["bodyWater"] <= 65
    ), "Invalid range for body water in total average"
    assert (
        2 <= weigh_ins_daily_data["totalAverage"]["boneMass"] <= 5
    ), "Invalid range for bone mass in total average"
    assert (
        30 <= weigh_ins_daily_data["totalAverage"]["muscleMass"] <= 60
    ), "Invalid range for muscle mass in total average"
    assert weigh_ins_daily_data["totalAverage"]["physiqueRating"] in [
        "Good",
        "Average",
        "Excellent",
    ], "Invalid physique rating in total average"
    assert (
        5 <= weigh_ins_daily_data["totalAverage"]["visceralFat"] <= 15
    ), "Invalid range for visceral fat in total average"
    assert (
        20 <= weigh_ins_daily_data["totalAverage"]["metabolicAge"] <= 60
    ), "Invalid range for metabolic age in total average"

    for summary in weigh_ins_daily_data["dateWeightList"]:
        assert 59 <= summary["weight"] <= 91, "Invalid range for daily weight summaries"
