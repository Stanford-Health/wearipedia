import datetime
import re
from math import ceil
from re import Match

import dateutil
import numpy as np
import pandas as pd
import pytz
import requests
from dateutil import tz
from tqdm import tqdm

__all__ = ["WhoopUser"]


class WhoopUser:
    def __init__(self, email, password):
        self.BASE_URL = "https://api-7.whoop.com/"
        self.AUTH_URL = self.BASE_URL + "oauth/token"
        self.login(email, password)
        self.header = {"Authorization": f"bearer {self.token}"}
        self.CYCLES_URL = f"users/{self.user_id}/cycles"
        self.HEART_RATE_URL = self.BASE_URL + f"users/{self.user_id}/metrics/heart_rate"
        self.HEALTH_METRICS_URL = (
            "https://api.prod.whoop.com/coaching-service/v1/health/metrics"
        )

        self.SEED = 1

    def create_fake_cycles_df(self):

        np.random.seed(self.SEED)

        cycles_df_syn = pd.DataFrame(
            columns=[
                "id",
                "day",
                "rMSSD",
                "resting_hr",
                "recovery_score",
                "n_naps",
                "sleep_need_baseline",
                "sleep_debt",
                "sleep_need_strain",
                "sleep_need_total",
                "sleep_quality_duration",
                "avg_hr",
                "kilojoules",
                "max_hr",
                "strain_score",
            ]
        )

        num_sleeps = 42
        cycles_df_syn.id = np.random.choice(
            range(1000), size=(num_sleeps,), replace=False
        )
        cycles_df_syn.day = [
            "2022-04-26",
            "2022-04-27",
            "2022-04-28",
            "2022-04-29",
            "2022-04-30",
            "2022-05-01",
            "2022-05-02",
            "2022-05-03",
            "2022-05-04",
            "2022-05-05",
            "2022-05-06",
            "2022-05-07",
            "2022-05-08",
            "2022-05-09",
            "2022-05-10",
            "2022-05-11",
            "2022-05-12",
            "2022-05-13",
            "2022-05-14",
            "2022-05-15",
            "2022-05-16",
            "2022-05-17",
            "2022-05-18",
            "2022-05-19",
            "2022-05-20",
            "2022-05-21",
            "2022-05-22",
            "2022-05-23",
            "2022-05-24",
            "2022-05-25",
            "2022-05-26",
            "2022-05-27",
            "2022-05-28",
            "2022-05-29",
            "2022-05-30",
            "2022-05-31",
            "2022-06-01",
            "2022-06-02",
            "2022-06-03",
            "2022-06-04",
            "2022-06-05",
            "2022-06-06",
        ]
        cycles_df_syn.recovery_score = np.clip(
            50 + 10 * np.random.randn(num_sleeps), 0, 100
        ).astype("int")

        cycles_df_syn.n_naps = np.random.poisson(0.5, size=num_sleeps)

        ms_hour_normal = lambda loc, scale: np.clip(
            (
                3600 * 1000 * np.random.normal(loc=loc, scale=scale, size=(num_sleeps,))
            ).astype("int"),
            0,
            None,
        )

        cycles_df_syn.sleep_need_baseline = ms_hour_normal(8, 1)
        cycles_df_syn.sleep_debt = ms_hour_normal(1, 0.2)
        cycles_df_syn.sleep_need_strain = ms_hour_normal(0.1, 0.1)
        cycles_df_syn.sleep_need_total = ms_hour_normal(8, 1)
        cycles_df_syn.sleep_quality_duration = ms_hour_normal(6, 1)

        cycles_df_syn.resting_hr = np.clip(
            np.random.normal(loc=60, scale=5, size=(num_sleeps,)).astype("int"), 0, None
        )
        cycles_df_syn.avg_hr = np.clip(
            np.random.normal(loc=70, scale=5, size=(num_sleeps,)).astype("int"), 0, None
        )
        cycles_df_syn.kilojoules = np.clip(
            np.random.normal(loc=9000, scale=1000, size=(num_sleeps,)), 0, None
        )
        cycles_df_syn.max_hr = np.clip(
            np.random.normal(loc=150, scale=10, size=(num_sleeps,)).astype("int"),
            0,
            200,
        )
        cycles_df_syn.strain_score = np.clip(
            np.random.normal(loc=12, scale=2, size=(num_sleeps,)), 0, 21
        )
        cycles_df_syn.rMSSD = np.clip(
            np.random.normal(loc=0.07, scale=0.01, size=(num_sleeps,)), 0, None
        )

        return cycles_df_syn

    def create_fake_metrics_df(self):

        np.random.seed(self.SEED)

        n_rows = 58

        metrics_df_syn = pd.DataFrame(
            columns=[
                "id",
                "day",
                "RESPIRATORY_RATE.current_value",
                "RESPIRATORY_RATE.current_deviation",
                "BLOOD_OXYGEN.current_value",
                "BLOOD_OXYGEN.current_deviation",
                "RHR.current_value",
                "RHR.current_deviation",
                "HRV.current_value",
                "HRV.current_deviation",
                "SKIN_TEMPERATURE_CELSIUS.current_value",
                "SKIN_TEMPERATURE_CELSIUS.current_deviation",
                "SKIN_TEMPERATURE_FAHRENHEIT.current_value",
                "SKIN_TEMPERATURE_FAHRENHEIT.current_deviation",
            ]
        )

        metrics_df_syn.id = np.random.choice(range(1000), size=(n_rows,), replace=False)

        metrics_df_syn.day = [
            "2022-04-25",
            "2022-04-26",
            "2022-04-27",
            "2022-04-28",
            "2022-04-29",
            "2022-04-30",
            "2022-05-01",
            "2022-05-02",
            "2022-05-03",
            "2022-05-04",
            "2022-05-05",
            "2022-05-06",
            "2022-05-07",
            "2022-05-08",
            "2022-05-09",
            "2022-05-10",
            "2022-05-11",
            "2022-05-12",
            "2022-05-13",
            "2022-05-14",
            "2022-05-15",
            "2022-05-16",
            "2022-05-17",
            "2022-05-18",
            "2022-05-19",
            "2022-05-20",
            "2022-05-21",
            "2022-05-22",
            "2022-05-23",
            "2022-05-24",
            "2022-05-25",
            "2022-05-26",
            "2022-05-27",
            "2022-05-28",
            "2022-05-29",
            "2022-05-30",
            "2022-05-31",
            "2022-06-01",
            "2022-06-02",
            "2022-06-03",
            "2022-06-04",
            "2022-06-05",
            "2022-06-06",
            "2022-06-22",
            "2022-06-23",
            "2022-06-25",
            "2022-06-26",
            "2022-06-28",
            "2022-06-29",
            "2022-06-30",
            "2022-07-01",
            "2022-07-03",
            "2022-07-05",
            "2022-07-07",
            "2022-07-09",
            "2022-07-10",
            "2022-07-12",
            "2022-07-14",
        ]

        metrics_df_syn["RESPIRATORY_RATE.current_value"] = np.clip(
            np.random.normal(loc=15, scale=1, size=(n_rows,)), 0, None
        )

        metrics_df_syn["RESPIRATORY_RATE.current_deviation"] = np.random.normal(
            loc=0, scale=0.5, size=(n_rows,)
        )
        metrics_df_syn["BLOOD_OXYGEN.current_value"] = np.clip(
            np.round(np.random.normal(loc=96, scale=1, size=(n_rows,))), 0, 100
        )
        metrics_df_syn["BLOOD_OXYGEN.current_deviation"] = np.clip(
            np.round(np.random.normal(loc=0, scale=0.8, size=(n_rows,))), -3, 3
        )
        metrics_df_syn["RHR.current_value"] = np.clip(
            np.round(np.random.normal(loc=60, scale=3, size=(n_rows,))), 0, None
        )
        metrics_df_syn["RHR.current_deviation"] = np.clip(
            np.round(np.random.normal(loc=0, scale=0.8, size=(n_rows,))), -3, 3
        )
        metrics_df_syn["HRV.current_value"] = np.clip(
            np.round(np.random.normal(loc=70, scale=3, size=(n_rows,))), 0, None
        )
        metrics_df_syn["HRV.current_deviation"] = np.clip(
            np.round(np.random.normal(loc=0, scale=4, size=(n_rows,))), -3, 3
        )
        metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_value"] = np.clip(
            np.random.normal(loc=33, scale=1.0, size=(n_rows,)), 0, None
        )
        metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_deviation"] = np.clip(
            np.random.normal(loc=0, scale=0.5, size=(n_rows,)), -3, 3
        )
        metrics_df_syn["SKIN_TEMPERATURE_FAHRENHEIT.current_value"] = (
            9 / 5 * metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_value"] + 32
        )
        metrics_df_syn["SKIN_TEMPERATURE_FAHRENHEIT.current_deviation"] = (
            9 / 5 * metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_deviation"]
        )

        return metrics_df_syn

    def create_fake_hr_df(self):  # heart rate depends on sleeps

        np.random.seed(self.SEED)

        # start_ts = 1651104000.0
        start_ts = 1650931200.0

        N = 275000

        sleeps_syn = self.sleeps_df

        hr_df_syn = pd.DataFrame(
            pd.np.empty((N, 2)) * pd.np.nan, columns=["heart_rate", "timestamp"]
        )

        heart_rate = np.random.normal(loc=80, scale=20, size=(N,)).astype("int")
        hr_df_syn.heart_rate = heart_rate

        hr_df_syn.timestamp = np.linspace(start_ts, start_ts + 7 * (N - 1), N)

        hr_df_syn.timestamp = hr_df_syn.timestamp.progress_apply(
            lambda x: datetime.datetime.fromtimestamp(
                x, tz=dateutil.tz.gettz("US/Pacific")
            )
        )

        for lower, upper, is_nap in tqdm(
            zip(
                sleeps_syn.time_lower_bound,
                sleeps_syn.time_upper_bound,
                sleeps_syn.is_nap,
            )
        ):
            lower_idx = int((lower.timestamp() - start_ts) // 7)
            upper_idx = int((upper.timestamp() - start_ts) // 7)

            decrement_val = 20 if is_nap else 40

            hr_df_syn.loc[lower_idx:upper_idx, ["heart_rate"]] -= decrement_val

        return hr_df_syn

    def create_fake_sleeps_df(self):

        np.random.seed(self.SEED)

        columns = [
            "cycle_id",
            "sleep_id",
            "cycles_count",
            "disturbance_count",
            "time_upper_bound",
            "time_lower_bound",
            "is_nap",
            "in_bed_duration",
            "light_sleep_duration",
            "latency_duration",
            "no_data_duration",
            "rem_sleep_duration",
            "respiratory_rate",
            "sleep_score",
            "sleep_efficiency",
            "sleep_consistency",
            "sws_duration",
            "wake_duration",
            "quality_duration",
        ]
        sleeps_syn = pd.DataFrame(columns=columns)
        num_sleeps = 43
        sleeps_syn.cycle_id = np.random.choice(
            range(1000), size=(num_sleeps,), replace=False
        )
        sleeps_syn.sleep_id = np.random.choice(
            range(1000), size=(num_sleeps,), replace=False
        )

        sleeps_syn.cycles_count = np.random.poisson(1, size=(num_sleeps,))
        sleeps_syn.disturbance_count = np.random.poisson(12, size=(num_sleeps,))
        sleeps_syn.is_nap = ([False, True] * num_sleeps)[:num_sleeps]

        dur = []
        for i in range(num_sleeps):
            dur.append(np.clip(np.random.normal(loc=8.0), 0, 14))
            dur.append(np.clip(np.random.normal(loc=1.0, scale=0.5), 0.2, 6))

        sleeps_syn.in_bed_duration = dur[
            :num_sleeps
        ]  # ([np.clip(np.random.exponential(scale=1.0), 0, 14), np.clip(np.random.exponential(scale=8.0), 0, 14)] * num_sleeps)[:num_sleeps]#np.clip(np.random.exponential(scale=8.0), 0, 14)
        sleeps_syn.light_sleep_duration = sleeps_syn.in_bed_duration * 0.5
        sleeps_syn.latency_duration = 0
        sleeps_syn.no_data_duration = 0
        sleeps_syn.rem_sleep_duration = sleeps_syn.in_bed_duration * 0.1
        sleeps_syn.sws_duration = sleeps_syn.in_bed_duration * 0.3
        sleeps_syn.wake_duration = sleeps_syn.in_bed_duration * 0.1
        sleeps_syn.quality_duration = sleeps_syn.in_bed_duration * 0.9
        sleeps_syn.respiratory_rate = np.random.normal(loc=15, size=(num_sleeps,))
        sleeps_syn.sleep_score = np.random.randint(0, 100, size=(num_sleeps,))
        sleeps_syn.sleep_efficiency = 0.90
        sleeps_syn.sleep_consistency = np.random.uniform(0, 1, size=(num_sleeps,))

        # create start/end times
        cur_timestamp = 1650960000.0

        sleep_starts = []
        sleep_ends = []

        # make sleep start/end correspond with duration
        for i in range(sleeps_syn.shape[0]):
            try:
                offset = int(sleeps_syn.iloc[i * 2].in_bed_duration * 3600)
                sleep_starts.append(cur_timestamp)
                sleep_ends.append(cur_timestamp + offset)

                offset = int(sleeps_syn.iloc[i * 2 + 1].in_bed_duration * 3600)
                sleep_starts.append(cur_timestamp + 14 * 3600)
                sleep_ends.append(cur_timestamp + 14 * 3600 + offset)
                cur_timestamp += 24 * 3600
            except:
                pass  # index error

        sleep_starts = [
            datetime.datetime.fromtimestamp(ts, tz=dateutil.tz.gettz("US/Pacific"))
            for ts in sleep_starts
        ]
        sleep_ends = [
            datetime.datetime.fromtimestamp(ts, tz=dateutil.tz.gettz("US/Pacific"))
            for ts in sleep_ends
        ]
        sleeps_syn.time_lower_bound = sleep_starts[:num_sleeps]
        sleeps_syn.time_upper_bound = sleep_ends[:num_sleeps]

        return sleeps_syn

    def login(self, email, password):
        """
        Login to whoop API, storing User id and token
        :param email: str email
        :param password: str password
        :return: None will set class variables
        """

        if len(email) == 0:  # fake the login
            self.token = ""
            self.user_id = ""
            return

        login = requests.post(
            self.AUTH_URL,
            json={
                "grant_type": "password",
                "issueRefresh": False,
                "password": password,
                "username": email,
            },
        )
        if login.status_code != 200:
            raise AssertionError("Credentials rejected")
        login_data = login.json()
        self.token = login_data["access_token"]
        self.user_id = login_data["user"]["id"]

    default_params = {
        "start": "2000-01-01T00:00:00.000Z",
        "end": "2030-01-01T00:00:00.000Z",
    }

    def get_health_metrics_json(self, cycle_id):
        """
        Get health metrics from your most recent sleep cycle.
        """

        metrics_request = requests.get(
            self.HEALTH_METRICS_URL + f"/{cycle_id}", headers=self.header
        )

        data = metrics_request.json()

        return data

    def get_health_metrics_df(self, params=default_params):

        if self.token == "":
            return self.create_fake_metrics_df()

        json_data = self.get_cycles_json(params=params)

        ids = [j["id"] for j in json_data]
        days = [j["days"][0] for j in json_data]

        df_list = []

        data = [self.get_health_metrics_json(cycle_id=id) for id in ids]

        for id, day, row in zip(ids, days, data):

            metric_dict = dict()

            metric_dict["id"] = id
            metric_dict["day"] = day

            for metric in row["health_monitor_metrics"]:
                name = metric["metric"]

                metric_dict[f"{name}.current_value"] = metric["current_value"]
                metric_dict[f"{name}.current_deviation"] = metric["current_deviation"]

            df_list.append(metric_dict)

        return pd.DataFrame.from_dict(df_list)

    def get_cycles_json(self, params=default_params):
        """
        Record base information
        :param params: start, end, other params
        :return: json with all info from cycles endpoint
        """
        cycles_URL = f"https://api-7.whoop.com/users/{self.user_id}/cycles"
        cycles_request = requests.get(cycles_URL, params=params, headers=self.header)
        return cycles_request.json()

    def get_cycles_df(self, params=default_params):
        """
        :param params: params for cycle query
        :return: dataframe with all the cycle info
        """

        if self.token == "":
            if not hasattr(self, "cycles_df"):
                self.cycles_df = self.create_fake_cycles_df()

            return self.cycles_df

        df_columns = [
            "id",
            "day",
            "rMSSD",
            "resting_hr",
            "recovery_score",
            "n_naps",
            "sleep_need_baseline",
            "sleep_debt",
            "sleep_need_strain",
            "sleep_need_total",
            "sleep_quality_duration",
            "avg_hr",
            "kilojoules",
            "max_hr",
            "strain_score",
        ]
        result_df = pd.DataFrame(columns=df_columns)
        json_data = self.get_cycles_json(params=params)
        for day in json_data:
            if not (
                day["recovery"]
                and "timestamp" in day["recovery"]
                and "heartRateVariabilityRmssd" in day["recovery"]
                and isinstance(
                    day["recovery"]["heartRateVariabilityRmssd"], (int, float)
                )
                and day["sleep"]
                and day["sleep"]["sleeps"]
                and day["sleep"]["sleeps"][0]["timezoneOffset"]
            ):
                continue
            day_data = day
            series_dict = {}
            series_dict["id"] = day_data["id"]
            series_dict["day"] = day_data["days"][0]
            series_dict["n_naps"] = len(day_data["sleep"]["naps"])
            recovery_data = day_data["recovery"]
            series_dict["rMSSD"] = recovery_data["heartRateVariabilityRmssd"]
            series_dict["resting_hr"] = recovery_data["restingHeartRate"]
            series_dict["recovery_score"] = recovery_data["score"]
            if day_data["sleep"]["needBreakdown"] is None:
                series_dict["sleep_need_baseline"] = 0
                series_dict["sleep_debt"] = 0
                series_dict["sleep_need_strain"] = 0
                series_dict["sleep_need_total"] = 0
            else:
                need_breakdown = day_data["sleep"]["needBreakdown"]
                series_dict["sleep_need_baseline"] = need_breakdown["baseline"]
                series_dict["sleep_debt"] = need_breakdown["debt"]
                series_dict["sleep_need_strain"] = need_breakdown["strain"]
                series_dict["sleep_need_total"] = need_breakdown["total"]
            series_dict["sleep_quality_duration"] = day_data["sleep"]["qualityDuration"]
            strain_data = day_data["strain"]
            series_dict["avg_hr"] = strain_data["averageHeartRate"]
            series_dict["kilojoules"] = strain_data["kilojoules"]
            series_dict["max_hr"] = strain_data["maxHeartRate"]
            series_dict["strain_score"] = strain_data["score"]
            result_df = result_df.append(series_dict, ignore_index=True)
        return result_df

    def get_sleeps_df(self, params=default_params, timezone="UTC"):
        """
        Will return all sleep data in a dataframe from the cycles endpoint. Done in a seperate method because there is a
        manyToOne type relationship between sleeps and cycles. In most cases there is just one, unless you;ve slept
        multiple times in a day
        :param params: start/end data
        :return: dataframe with sleep data, linked to cycles IDs
        """

        if self.token == "":
            if not hasattr(self, "sleeps_df"):
                self.sleeps_df = self.create_fake_sleeps_df()

            return self.sleeps_df

        df_cols = [
            "cycle_id",
            "sleep_id",
            "cycles_count",
            "disturbance_count",
            "time_lower_bound",
            "time_upper_bound",
            "in_bed_duration",
            "is_nap",
            "latency_duration",
            "light_sleep_duration",
            "no_data_duration",
            "quality_duration",
            "rem_sleep_duration",
            "respiratory_rate",
            "sleep_score",
            "sleep_consistency",
            "sleep_efficiency",
            "sws_duration",
            "wake_duration",
        ]

        def localize(ts):
            utc = datetime.datetime.strptime(
                ts.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
            )
            from_zone = tz.gettz("UTC")
            to_zone = tz.gettz(timezone)

            utc = utc.replace(tzinfo=from_zone)

            # Convert time zone
            localized = utc.astimezone(to_zone)

            return localized

        result_df = pd.DataFrame(columns=df_cols)
        cycles_data = self.get_cycles_json(params)
        df_dict_list = []
        for day in cycles_data:
            if day["sleep"]["id"] is None:
                continue
            sleep_data = day["sleep"]["naps"] + day["sleep"]["sleeps"]
            if len(sleep_data) == 0:
                continue
            cycle_id = day["id"]
            for sleep in sleep_data:
                row_dict = {}
                row_dict["cycle_id"] = cycle_id
                row_dict["sleep_id"] = sleep["id"]
                row_dict["cycles_count"] = sleep["cyclesCount"]
                row_dict["disturbance_count"] = sleep["disturbanceCount"]
                # for some reason whoop leaves all timezone substrings in the
                # datetime string as +0000, and adds a timezone offset field
                # to the response
                tz_as_str = sleep["timezoneOffset"]
                row_dict["time_upper_bound"] = localize(
                    WhoopUser.convert_whoop_str_to_datetime(
                        sleep["during"]["upper"], tz_as_str
                    )
                )
                row_dict["time_lower_bound"] = localize(
                    WhoopUser.convert_whoop_str_to_datetime(
                        sleep["during"]["lower"], tz_as_str
                    )
                )
                row_dict["is_nap"] = sleep["isNap"]
                row_dict["in_bed_duration"] = sleep["inBedDuration"]
                row_dict["light_sleep_duration"] = sleep["lightSleepDuration"]
                row_dict["latency_duration"] = sleep["latencyDuration"]
                row_dict["no_data_duration"] = sleep["noDataDuration"]
                row_dict["rem_sleep_duration"] = sleep["remSleepDuration"]
                row_dict["respiratory_rate"] = sleep["respiratoryRate"]
                row_dict["sleep_score"] = sleep["score"]
                row_dict["sleep_efficiency"] = sleep["sleepEfficiency"]
                row_dict["sleep_consistency"] = sleep["sleepConsistency"]
                row_dict["sws_duration"] = sleep["slowWaveSleepDuration"]
                row_dict["wake_duration"] = sleep["wakeDuration"]
                row_dict["quality_duration"] = sleep["qualityDuration"]
                df_dict_list.append(row_dict)
        result_df = pd.DataFrame.from_dict(df_dict_list)
        return result_df

    def get_workouts_df(self, params=default_params):
        """
        Will get all data related to workouts.

        Dataframe will link to cycle IDs
        :param params: start end date
        :return: dataframe
        """
        cycles_data = self.get_cycles_json()
        df_cols = [
            "cycle_id",
            "workout_id",
            "average_hr",
            "cumulative_strain",
            "time_upper_bound",
            "time_lower_bound",
            "kilojoules",
            "strain_score",
            "sport_id",
            "source",
            "time_hr_zone_0",
            "time_hr_zone_1",
            "time_hr_zone_2",
            "time_hr_zone_3",
            "time_hr_zone_4",
            "time_hr_zone_5",
        ]
        result_df = pd.DataFrame(columns=df_cols)
        for day in cycles_data:
            cycle_id = day["id"]
            workout_data = day["strain"]["workouts"]
            if len(workout_data) == 0:
                continue
            for workout in workout_data:
                row_dict = {}
                row_dict["cycle_id"] = cycle_id
                row_dict["workout_id"] = workout["id"]
                row_dict["average_hr"] = workout["averageHeartRate"]
                row_dict["cumulative_strain"] = workout["cumulativeWorkoutStrain"]
                row_dict["time_upper_bound"] = workout["during"]["upper"]
                row_dict["time_lower_bound"] = workout["during"]["lower"]
                row_dict["kilojoules"] = workout["kilojoules"]
                row_dict["strain_score"] = workout["score"]
                row_dict["sport_id"] = workout["sportId"]
                row_dict["source"] = workout["source"]
                zones = workout["zones"]
                for i in range(0, 6):
                    row_dict["time_hr_zone_" + str(i)] = zones[i]
                result_df = result_df.append(row_dict, ignore_index=True)
        return result_df

    default_params_hr = {
        "start": "2022-04-24T00:00:00.000Z",
        "end": "2022-04-28T00:00:00.000Z",
    }

    def get_heart_rate_json(self, params=default_params_hr):
        """
        Get heart rate data on user
        :param params: params for heart rate data
        :return: dict of heart rate data
        """
        hr_request = requests.get(
            self.HEART_RATE_URL, params=params, headers=self.header
        )
        data = hr_request.json()
        return data

    def get_heart_rate_df(
        self, params=default_params_hr, timezone="UTC", verbose=False
    ):
        """
        Get heart rate data as a dataframe. Note the maximum range is 8 days.

        Converts thirteen digit UNIX timestamp to
        normal time.
        Can take a very long time to run depending on how many days are specified.
        Maybe optimize later
        :param params: start end range
        :return:dataframe with heart rate data over time
        """

        if self.token == "":
            if not hasattr(self, "sleeps_df"):
                self.sleeps_df = self.create_fake_sleeps_df()

            if not hasattr(self, "hr_df"):
                self.hr_df = self.create_fake_hr_df()

            start_time = dateutil.parser.parse(params["start"])
            end_time = dateutil.parser.parse(params["end"])

            bool_mask = self.hr_df.timestamp.progress_apply(
                lambda x: start_time < x and x < end_time
            )

            hr_df = self.hr_df[bool_mask]

            return hr_df

        def tick_time_to_local_timezone(tick_time):
            current = WhoopUser.convert_unix_time_to_current(tick["time"])
            dt_obj = datetime.datetime.strptime(current, "%Y-%m-%d %H:%M:%S")

            local_timezone = pytz.timezone(timezone)
            local_datetime = dt_obj.replace(tzinfo=pytz.utc)
            local_datetime = local_datetime.astimezone(local_timezone)

            return local_datetime

        def split_into_weeklong_params(params):
            end = datetime.datetime.strptime(
                params["end"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
            )
            start = datetime.datetime.strptime(
                params["start"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
            )

            if end > datetime.datetime.now():
                end = datetime.datetime.now()

            all_params = []
            for i in range(ceil((end - start).days / 7)):
                segment_start = start + datetime.timedelta(days=7 * i)
                segment_end = start + datetime.timedelta(days=7 * (i + 1))

                all_params.append(
                    {
                        "start": segment_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "end": segment_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    }
                )

            return all_params

        split_params = split_into_weeklong_params(params)

        data = []

        if verbose:
            split_params = tqdm(split_params)

        for p in split_params:
            data = data + self.get_heart_rate_json(p)["values"]

        result_df = pd.DataFrame(columns=["heart_rate", "timestamp"])
        df_dict_list = []
        for tick in data:
            row_dict = {}
            row_dict["heart_rate"] = tick["data"]
            row_dict["timestamp"] = tick_time_to_local_timezone(tick["time"])
            # result_df = result_df.append(row_dict, ignore_index=True)
            df_dict_list.append(row_dict)
        result_df = pd.DataFrame.from_dict(df_dict_list)
        return result_df

    @staticmethod
    def convert_unix_time_to_current(timestamp):
        """will use local timezone for moment."""
        time = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convert_whoop_str_to_datetime(whoop_dt: str, tz: str) -> datetime.datetime:
        """
        Make proper datetimes out of this.

        sometimes microseconds are given with 2 digits, not 3
        pad with zero if necessary
        """

        def zero_pad_microseconds(mseconds: Match) -> str:
            return f".{mseconds.group(1).ljust(3, '0')}+"

        adjusted_str = re.sub(r"\.([0-9]{0,3})\+", zero_pad_microseconds, whoop_dt)

        def correct_tz(tz_match: Match) -> str:
            return f"{tz[:3]}:{tz[3:]}"

        final_str = re.sub(r"([\+|\-][0-9]{2}:[0-9]{2})", correct_tz, adjusted_str)

        return datetime.datetime.fromisoformat(final_str)

    def get_sports(self):
        """:return: List of sports and releveant information."""
        sports_url = self.BASE_URL + "sports"
        sports_request = requests.get(sports_url, headers=self.header)
        return sports_request.json()
