from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def create_syn_data(start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    steps = {}
    calories = {}
    bpm = {}
    brpm = {}
    spo2 = {}

    current_time = start_date_obj
    while start_date_obj <= end_date_obj:
        date = start_date_obj.strftime("%Y-%m-%d")

        # Simulate steps and calories (missing data simulated as zero)
        steps[date] = (
            np.random.poisson(5000) if np.random.random() < 0.8 else 0
        )  # average 5000 steps a day
        calories[date] = (
            np.random.normal(2500, 500) if np.random.random() < 0.8 else 0
        )  # average 2500 calories a day

        while current_time < start_date_obj + timedelta(days=1):
            # Simulate bpm every second (missing data simulated as no entry)
            if np.random.random() < 0.7:  # assume data for 70% of the time
                time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                bpm[time] = np.random.normal(70, 10)  # average bpm 70

            current_time += timedelta(seconds=1)

        # Simulate brpm and spo2 every 10 mins (missing data simulated as no entry)
        current_time = start_date_obj
        while current_time < start_date_obj + timedelta(days=1):
            if np.random.random() < 0.7:  # assume data for 70% of the time
                time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                brpm[time] = np.random.normal(15, 2)  # average brpm 15
                spo2[time] = np.random.normal(98, 1)  # average spo2 98%

            current_time += timedelta(minutes=10)

        start_date_obj += timedelta(days=1)

    return steps, calories, bpm, brpm, spo2
