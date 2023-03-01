from datetime import datetime

import numpy as np
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_vantage(real):

    start_dates = [
        np.datetime64("2009-11-15"),
        np.datetime64("2021-04-01"),
        np.datetime64("2022-06-10"),
    ]
    end_dates = [
        np.datetime64("2010-02-01"),
        np.datetime64("2021-06-20"),
        np.datetime64("2022-12-10"),
    ]

    for start_date, end_date in zip(start_dates, end_dates):

        device = wearipedia.get_device(
            "polar/vantage",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        # This training id is only valid for arjo@stanford.edu
        params = {
            "start_date": str(start_date),
            "end_date": str(end_date),
            "training_id": "7472390363",
        }

        if real:
            wearipedia._authenticate_device("polar/vantage", device)

        sleep = device.get_data("sleep", params=params)
        training_history = device.get_data("training_history", params=params)
        training_by_id = []
        try:
            # Just in case the training id is not valid, we don't want to fail the test
            training_by_id = device.get_data("training_by_id", params=params)
        except:
            pass

        sleep_helper(sleep)
        training_history_helper(training_history)
        training_by_id_helper(training_by_id)


def sleep_helper(data):
    for d in data:
        assert list(d.keys()) == [
            "date",
            "sleepStartTime",
            "sleepEndTime",
            "sleepStartOffset",
            "sleepEndOffset",
            "sleepRating",
            "continuityIndex",
            "continuityClass",
            "sleepCycles",
            "sleepScore",
            "sleepWakeStates",
        ]
        assert isinstance(d["date"], str)
        assert isinstance(d["sleepStartTime"], str)
        assert len(d["sleepStartTime"].split(":")) == 4
        assert isinstance(d["sleepEndTime"], str)
        assert len(d["sleepEndTime"].split(":")) == 4
        assert d["sleepCycles"] is None or isinstance(d["sleepCycles"], int)
        assert d["sleepScore"] is None or isinstance(d["sleepScore"], float)
        assert d["sleepWakeStates"] is None or isinstance(d["sleepWakeStates"], list)


def training_history_helper(data):
    for d in data:
        assert list(d.keys()) == [
            "id",
            "duration",
            "distance",
            "hrAvg",
            "calories",
            "note",
            "sportName",
            "sportId",
            "startDate",
            "recoveryTime",
            "iconUrl",
            "trainingLoadHtml",
            "hasTrainingTarget",
            "swimmingSport",
            "swimmingPoolUnits",
            "trainingLoadProHtml",
            "periodDataUuid",
            "isTest",
        ]
        assert isinstance(d["id"], int)
        assert d["duration"] == None or isinstance(d["duration"], int)
        assert d["distance"] == None or isinstance(d["distance"], (float, int))
        assert d["hrAvg"] == None or isinstance(d["hrAvg"], int)
        assert d["calories"] == None or (
            isinstance(d["calories"], int) and d["calories"] >= 0
        )
        assert d["note"] == None or isinstance(d["note"], str)
        assert isinstance(d["sportName"], str)
        assert isinstance(d["sportId"], int)
        assert isinstance(d["startDate"], str)
        assert isinstance(d["recoveryTime"], int)
        assert isinstance(d["iconUrl"], str)
        assert isinstance(d["trainingLoadHtml"], str)
        assert isinstance(d["hasTrainingTarget"], bool)
        assert isinstance(d["swimmingSport"], bool)
        assert d["swimmingPoolUnits"] == None or isinstance(d["swimmingPoolUnits"], str)
        assert isinstance(d["trainingLoadProHtml"], str)
        assert d["periodDataUuid"] == None or isinstance(d["periodDataUuid"], str)
        assert isinstance(d["isTest"], bool)
        assert d["hrAvg"] == None or (d["hrAvg"] >= 0 and d["hrAvg"] <= 255)


def training_by_id_helper(data):
    if data != None:
        d = data
        if len(data) > 0:
            assert list(d[0].keys()) == [
                "Name",
                "Sport",
                "Date",
                "Start time",
                "Duration",
                "Total distance (mi)",
                "Average heart rate (bpm)",
                "Average speed (mi/h)",
                "Max speed (mi/h)",
                "Average pace (min/mi)",
                "Max pace (min/mi)",
                "Calories",
                "Fat percentage of calories(%)",
                "Carbohydrate percentage of calories(%)",
                "Protein percentage of calories(%)",
                "Average cadence (rpm)",
                "Average stride length (in)",
                "Running index",
                "Training load",
                "Ascent (ft)",
                "Descent (ft)",
                "Average power (W)",
                "Max power (W)",
                "Notes",
                "Height (ft in)",
                "Weight (lbs)",
                "HR max",
                "HR sit",
                "VO2max",
                "Unnamed: 29",
            ]
            assert isinstance(d[0]["Name"], str)
            assert isinstance(d[0]["Sport"], str)
            assert isinstance(d[0]["Date"], str)
            assert isinstance(d[0]["Start time"], str)
            assert isinstance(d[0]["Duration"], str)
            if d[0]["Total distance (mi)"] != None:
                assert isinstance(d[0]["Total distance (mi)"], (float, int))
            if d[0]["Average heart rate (bpm)"] != None:
                assert isinstance(d[0]["Average heart rate (bpm)"], (float, int))
                assert (
                    d[0]["Average heart rate (bpm)"] >= 0
                    and d[0]["Average heart rate (bpm)"] <= 255
                )
            if d[0]["Average speed (mi/h)"] != None:
                assert isinstance(d[0]["Average speed (mi/h)"], (float, int))
            if d[0]["Max speed (mi/h)"] != None:
                assert isinstance(d[0]["Max speed (mi/h)"], (float, int))
            if d[0]["Average pace (min/mi)"] != None:
                assert isinstance(d[0]["Average pace (min/mi)"], (float, int))
            if d[0]["Max pace (min/mi)"] != None:
                assert isinstance(d[0]["Max pace (min/mi)"], (float, int))
            if d[0]["Calories"] != None:
                assert isinstance(d[0]["Calories"], (float, int))
                assert d[0]["Calories"] >= 0
            if d[0]["Fat percentage of calories(%)"] != None:
                assert isinstance(d[0]["Fat percentage of calories(%)"], (int, float))
                assert (
                    d[0]["Fat percentage of calories(%)"] >= 0
                    and d[0]["Fat percentage of calories(%)"] <= 100
                )
            if d[0]["Carbohydrate percentage of calories(%)"] != None:
                assert isinstance(
                    d[0]["Carbohydrate percentage of calories(%)"], (int, float)
                )
                assert (
                    d[0]["Carbohydrate percentage of calories(%)"] >= 0
                    and d[0]["Carbohydrate percentage of calories(%)"] <= 100
                )
            if d[0]["Protein percentage of calories(%)"] != None:
                assert isinstance(
                    d[0]["Protein percentage of calories(%)"], (int, float)
                )
                assert (
                    d[0]["Protein percentage of calories(%)"] >= 0
                    and d[0]["Protein percentage of calories(%)"] <= 100
                )
            if d[0]["Average cadence (rpm)"] != None:
                assert isinstance(d[0]["Average cadence (rpm)"], (int, float))
            if d[0]["Average stride length (in)"] != None:
                assert isinstance(d[0]["Average stride length (in)"], (int, float))
            if d[0]["Running index"] != None:
                assert isinstance(d[0]["Running index"], (int, float))
            if d[0]["Training load"] != None:
                assert isinstance(d[0]["Training load"], (int, float))
            if d[0]["Ascent (ft)"] != None:
                assert isinstance(d[0]["Ascent (ft)"], (int, float))
            if d[0]["Descent (ft)"] != None:
                assert isinstance(d[0]["Descent (ft)"], (int, float))
            if d[0]["Average power (W)"] != None:
                assert isinstance(d[0]["Average power (W)"], (int, float))
            if d[0]["Max power (W)"] != None:
                assert isinstance(d[0]["Max power (W)"], (int, float))
            if d[0]["Notes"] != None:
                assert isinstance(d[0]["Notes"], (str, float))
            if d[0]["Height (ft in)"] != None:
                assert isinstance(d[0]["Height (ft in)"], str)
            if d[0]["Weight (lbs)"] != None:
                assert isinstance(d[0]["Weight (lbs)"], (int, float))
            if d[0]["HR max"] != None:
                assert isinstance(d[0]["HR max"], (int, float))
                assert d[0]["HR max"] >= 0 and d[0]["HR max"] <= 255
            if d[0]["HR sit"] != None:
                assert isinstance(d[0]["HR sit"], (int, float))
                assert d[0]["HR sit"] >= 0 and d[0]["HR sit"] <= 255
            if d[0]["VO2max"] != None:
                assert isinstance(d[0]["VO2max"], (int, float))
                assert d[0]["VO2max"] >= 0 and d[0]["VO2max"] <= 100
            assert list(d[1].keys()) == [
                "Sample rate",
                "Time",
                "HR (bpm)",
                "Speed (mi/h)",
                "Pace (min/mi)",
                "Cadence",
                "Altitude (ft)",
                "Stride length (in)",
                "Distances (ft)",
                "Temperatures (F)",
                "Power (W)",
                "Unnamed: 11",
            ]
