import pandas as pd
import numpy as np
import uuid

def create_syn_data(start_date,end_date):
    
    # create a list of dates between start and end date
    dates = pd.date_range(start_date, end_date)

    # {'id': 7472390363, 'duration': 3891594, 'distance': None, 'hrAvg': 120, 'calories': 409, 'note': ' ', 'sportName': 'Strength training', 'sportId': 15, 'startDate': '2022-08-27 17:59:56.956', 'recoveryTime': 37920000, 'iconUrl': 'https://platform.cdn.polar.com/ecosystem/sport/icon/d1ce94078aec226be28f6c602e6803e1-2015-10-20_13_45_19', 'trainingLoadHtml': '', 'hasTrainingTarget': False, 'swimmingSport': False, 'swimmingPoolUnits': 'METERS', 'trainingLoadProHtml': '000000', 'periodDataUuid': '9dc40412-815c-4037-86ca-6340a0b6e0b2', 'isTest': False}

    # create random id
    random_id = np.random.randint(1000000000,9999999999)

    # create random duration in milliseconds between 15 and 120 minutes
    random_duration = np.random.randint(900000,7200000)

    # create random distance 
    random_distance =  random_duration / 6000 * 5

    # create random hrAvg
    random_hrAvg = np.random.randint(60,180)

    # create random calories with the assumption that 1 
    random_calories = random_duration / 6000 * 5 * 0.1

    # create random recoveryTime
    random_recoveryTime = random_duration - np.random.randint(0,random_duration)

    # create random periodDataUuid
    random_periodDataUuid = str(uuid.uuid4())

    




