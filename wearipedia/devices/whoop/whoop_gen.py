# utils for generating synthetic data

from datetime import datetime, timedelta

import numpy as np

__all__ = [
    "create_fake_cycles",
    "create_fake_hr",
]


def create_fake_cycles(start_date, end_date):
    num_cycles = (end_date - start_date).days

    records = []

    for i in range(num_cycles):
        day = end_date - timedelta(days=i + 1)

        cycle = {
            "id": np.random.randint(0, 1000000000),
            "created_at": "2022-04-27T16:28:30.523+0000",
            "updated_at": "2022-08-19T17:10:29.456+0000",
            "scaled_strain": np.clip(0, 30, np.random.normal() * 5 + 10),
            "during": "['2022-04-27T11:42:16.060Z','2022-04-28T12:41:13.254Z')",
            "user_id": 4005531,
            "sleep_need": None,
            "predicted_end": "2022-04-28T12:41:13.254+0000",
            "timezone_offset": "-0700",
            "days": f"['{datetime.strftime(day, '%Y-%m-%d')}','{datetime.strftime(day + timedelta(days=1), '%Y-%m-%d')}')",
            "intensity_score": None,
            "data_state": "complete",
            "day_strain": np.clip(0, 0.01, np.random.normal() * 0.005 + 0.005),
            "day_kilojoules": np.random.normal() * 2500 + 5000,
            "day_avg_heart_rate": np.random.normal() * 10 + 75,
            "day_max_heart_rate": np.random.normal() * 20 + 150,
        }

        # overly simplistic model for now
        # TODO: change this so that it matches the
        # notebook
        num_sleeps = np.random.poisson(1)

        sleeps = []

        for _ in range(num_sleeps):
            sleep = {
                "cycle_id": np.random.randint(0, 1000000000),
                "created_at": "2022-04-27T01:47:48.706+0000",
                "updated_at": "2022-04-27T03:25:23.600+0000",
                "activity_id": np.random.randint(0, 1000000000),
                "score": int(np.random.uniform(0, 100)),
                "quality_duration": int(
                    np.clip(0, 50_000_000, np.random.normal() * 5_000_000 + 25_000_000)
                ),
                "latency": 0,
                "max_heart_rate": None,
                "average_heart_rate": None,
                "debt_pre": np.random.normal() * 100_000 + 3_000_000.0,
                "debt_post": np.random.normal() * 100_000 + 3_000_000.0,
                "need_from_strain": np.random.normal() * 100_000 + 3_000_000.0,
                "sleep_need": np.random.normal() * 100_000 + 3_000_000.0,
                "habitual_sleep_need": np.random.normal() * 100_000 + 3_000_000.0,
                "disturbances": 1,
                "time_in_bed": np.random.normal() * 100_000 + 3_000_000.0,
                "light_sleep_duration": np.random.normal() * 100_000 + 3_000_000,
                "slow_wave_sleep_duration": int(
                    np.random.normal() * 100_000 + 3_000_000
                ),
                "rem_sleep_duration": int(np.random.normal() * 100_000 + 3_000_000),
                "cycles_count": 1,
                "wake_duration": np.clip(
                    0, 1_000_000, int(np.random.normal() * 100_000 + 100_000)
                ),
                "arousal_time": np.random.normal() * 50_000 + 100_000,
                "no_data_duration": 0,
                "in_sleep_efficiency": np.random.uniform(0, 1),
                "credit_from_naps": 0.0,
                "hr_baseline": None,
                "respiratory_rate": np.random.normal() * 10 + 15.0,
                "sleep_consistency": None,
                "algo_version": "5.0.0",
                "projected_score": np.random.uniform(0, 100),
                "projected_sleep": 4281596.0,
                "optimal_sleep_times": None,
                "kilojoules": None,
                "user_id": np.random.randint(0, 1000000000),
                "during": "['2022-04-27T00:03:38.208Z','2022-04-27T01:20:41.151Z')",
                "timezone_offset": "-0700",
                "survey_response_id": None,
                "percent_recorded": 1.0,
                "auto_detected": True,
                "state": "complete",
                "responded": False,
                "team_act_id": None,
                "source": "auto+user",
                "is_significant": False,
                "is_normal": True,
                "is_nap": True,
            }

            sleeps.append(sleep)

        recovery = {
            "during": "['2022-04-27T11:42:16.060Z','2022-04-27T18:17:23.904Z')",
            "id": np.random.randint(0, 1000000000),
            "created_at": "2022-04-27T16:28:30.523+0000",
            "updated_at": "2022-04-27T18:49:22.756+0000",
            "date": "2022-04-27T18:17:23.904+0000",
            "user_id": np.random.randint(0, 1000000000),
            "sleep_id": np.random.randint(0, 1000000000),
            "survey_response_id": None,
            "cycle_id": np.random.randint(0, 1000000000),
            "responded": False,
            "recovery_score": int(np.random.uniform(0, 100)),
            "resting_heart_rate": int(np.random.uniform(45, 65)),
            "hrv_rmssd": 0.071095094,
            "state": "complete",
            "calibrating": True,
            "prob_covid": None,
            "hr_baseline": 57.0,
            "skin_temp_celsius": np.round(np.random.uniform(25, 40), 1),
            "spo2": np.round(np.random.uniform(70, 100), 1),
            "algo_version": "5.0.0",
            "rhr_component": None,
            "hrv_component": None,
            "history_size": 2.0,
            "from_sws": False,
            "recovery_rate": np.clip(0, 10, np.random.normal() * 2 + 3.5),
            "is_normal": None,
        }

        record = {
            "cycle": cycle,
            "sleeps": sleeps,
            "recovery": recovery,
            "workouts": [],
            "v2_activities": [],
        }

        records.append(record)

    return {"total_count": num_cycles, "offset": num_cycles, "records": records}


def create_fake_hr(start_date, end_date):
    # samples every minute now, for some reason

    values = []

    cur_timestamp = start_date

    while True:
        if cur_timestamp > end_date:
            break

        values.append(
            {"data": np.random.normal() * 20 + 80, "time": cur_timestamp.timestamp()}
        )
        cur_timestamp += timedelta(seconds=60.563)

    return {"name": "heart_rate", "start": start_date.timestamp(), "values": values}
