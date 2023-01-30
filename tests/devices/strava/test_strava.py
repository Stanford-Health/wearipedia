from datetime import datetime

import numpy as np
import pytest
import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_strava(real):
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
            "strava/strava",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        start_date = '2022-03-01'  # @param {type:"string"}
        end_date = '2022-06-17'  # @param {type:"string"}

        params = {"start_date": start_date, "end_date": end_date}

        if real:
            wearipedia._authenticate_device("strava/strava", device)

        distance = device.get_data("distance", params=params)

        moving_time = device.get_data("moving_time", params=params)

        elapsed_time = device.get_data("elapsed_time", params=params)

        total_elevation_gain = device.get_data(
            "total_elevation_gain", params=params)

        average_speed = device.get_data("average_speed", params=params)

        max_speed = device.get_data("max_speed", params=params)

        average_heartrate = device.get_data("average_heartrate", params=params)

        max_heartrate = device.get_data("max_heartrate", params=params)

        map_summary_polyline = device.get_data(
            "map_summary_polyline", params=params)

        elev_high = device.get_data("elev_high", params=params)

        elev_low = device.get_data("elev_low",  params=params)

        average_cadence = device.get_data("average_cadence", params=params)

        average_watts = device.get_data("average_watts", params=params)

        kilojoules = device.get_data("kilojoules", params=params)

        # run tests for device
        distance_helper(distance, start_date, end_date, real)
        moving_time_helper(moving_time, start_date, end_date, real)
        elapsed_time_helper(elapsed_time, start_date, end_date, real)
        total_elevation_gain_helper(
            total_elevation_gain, start_date, end_date, real)
        average_speed_helper(average_speed, start_date, end_date, real)
        max_speed_helper(max_speed, start_date, end_date, real)
        average_heartrate_helper(average_heartrate, start_date, end_date, real)
        max_heartrate_helper(max_heartrate, start_date, end_date, real)
        polyline_helper(
            map_summary_polyline, start_date, end_date, real)
        elev_high_helper(elev_high, start_date, end_date, real)
        elev_low_helper(elev_low, start_date, end_date, real)
        average_cadence_helper(average_cadence, start_date, end_date, real)
        average_watts_helper(average_watts, start_date, end_date, real)
        kilojoules_helper(kilojoules, start_date, end_date, real)


def basehelper(d):
    assert datetime.strptime(d['start_date'][:10], '%Y-%m-%d').date(
    ), f"Expected start_date to be a valid datetime, but got {d['start_date']}"

    assert type(
        d['name']) == str, f"Expected name to be a string, but got {type(d['name'])}"
    assert type(
        d['id']) == int, f"Expected type to be a integer, but got {type(d['id'])}"


def distance_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['distance']) == False:
            assert d['distance'] >= 0, f"Expected distance to be positive, but got {d['distance']}"
            assert d[
                'distance'] < 100000, f"Expected distance to be less than 100000, but got {d['distance']}"
        basehelper(d)


def moving_time_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['moving_time']) == False:
            assert d[
                'moving_time'] >= 0, f"Expected moving time to be positive, but got {d['moving_time']}"
            assert d[
                'moving_time'] < 14400, f"Expected moving time to be less than 4 hours, but got {d['distance']}"
        basehelper(d)


def elapsed_time_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['elapsed_time']) == False:
            assert d[
                'elapsed_time'] >= 0, f"Expected elapsed time to be positive, but got {d['elapsed_time']}"
            assert d[
                'elapsed_time'] < 14400, f"Expected elapsed time to be less than 4 hours, but got {d['distance']}"
        basehelper(d)


def total_elevation_gain_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['total_elevation_gain']) == False:
            assert d[
                'total_elevation_gain'] >= 0, f"Expected total_elevation_gain to be positive, but got {d['total_elevation_gain']}"
            assert d[
                'total_elevation_gain'] < 10000, f"Expected total_elevation_gain to be less than 10000, but got {d['total_elevation_gain']}"
        basehelper(d)


def average_speed_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['average_speed']) == False:
            assert d[
                'average_speed'] >= 0, f"Expected average_speed to be positive, but got {d['average_speed']}"
            assert d[
                'average_speed'] < 100, f"Expected average speed to be less than 100, but got {d['average_speed']}"
        basehelper(d)


def max_speed_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['max_speed']) == False:
            assert d[
                'max_speed'] >= 0, f"Expected max_speed to be positive, but got {d['max_speed']}"
            assert d[
                'max_speed'] < 100, f"Expected max_speed to be less than 100, but got {d['max_speed']}"
        basehelper(d)


def average_heartrate_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['average_heartrate']) == False:
            assert d[
                'average_heartrate'] >= 0, f"Expected average_heartrate to be positive, but got {d['average_heartrate']}"
            assert d[
                'average_heartrate'] < 200, f"Expected average_heartrate to be less than 200, but got {d['average_heartrate']}"
        basehelper(d)


def max_heartrate_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['max_heartrate']) == False:
            assert d[
                'max_heartrate'] >= 0, f"Expected max_heartrate to be positive, but got {d['max_heartrate']}"
            assert d[
                'max_heartrate'] < 300, f"Expected max_heartrate to be less than 300, but got {d['max_heartrate']}"
        basehelper(d)


def elev_high_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['elev_high']) == False:
            assert d[
                'elev_high'] >= 0, f"Expected elev_high to be positive, but got {d['elev_high']}"
            assert d[
                'elev_high'] < 10000, f"Expected elev_high to be less than 10000, but got {d['elev_high']}"
        basehelper(d)


def elev_low_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['elev_low']) == False:
            assert d[
                'elev_low'] >= 0, f"Expected elev_low to be positive, but got {d['elev_low']}"
            assert d[
                'elev_low'] < 10000, f"Expected elev_low to be less than 10000, but got {d['elev_low']}"
        basehelper(d)


def polyline_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if d['map.summary_polyline'] != None:
            assert type(d[
                'map.summary_polyline']) == str, f"Expected polyline to be stored as a stirng, but got {type(d['map.summary_polyline'])}"
        basehelper(d)


def average_cadence_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['average_cadence']) == False:
            assert d[
                'average_cadence'] >= 0, f"Expected average_cadence to be positive, but got {d['average_cadence']}"
            assert d[
                'average_cadence'] < 200, f"Expected average_cadence to be less than 200, but got {d['average_cadence']}"
        basehelper(d)


def average_watts_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['average_watts']) == False:
            assert d[
                'average_watts'] >= 0, f"Expected average_watts to be positive, but got {d['average_watts']}"
            assert d[
                'average_watts'] < 1000, f"Expected average_watts to be less than 1000, but got {d['average_watts']}"
        basehelper(d)


def max_watts_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['max_watts']) == False:
            assert d[
                'max_watts'] >= 0, f"Expected max_watts to be positive, but got {d['max_watts']}"
            assert d[
                'max_watts'] < 1000, f"Expected max_watts to be less than 1000, but got {d['max_watts']}"
        basehelper(d)


def kilojoules_helper(data, start_synthetic, end_synthetic, real):
    for d in data:
        if np.isnan(d['kilojoules']) == False:
            assert d[
                'kilojoules'] >= 0, f"Expected kilojoules to be positive, but got {d['kilojoules']}"
            assert d[
                'kilojoules'] < 100000, f"Expected kilojoules to be less than 100000, but got {d['kilojoules']}"
        basehelper(d)
