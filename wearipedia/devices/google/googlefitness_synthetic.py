import pandas as pd
import numpy as np

# Storing the general data source ids for the different data types
datasourceids = {
    'steps': 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
    'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm',
    'height': 'derived:com.google.height:com.google.android.gms:merge_height',
    'weight': 'derived:com.google.weight:com.google.android.gms:merge_weight',
    'speed': 'derived:com.google.speed:com.google.android.gms:merge_speed',
    'heart_minutes': 'derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes',
    'calories_expended': 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',
    'sleep': 'derived:com.google.sleep.segment:com.google.android.gms:merged',
    'blood_pressure': 'derived:com.google.blood_pressure:com.google.android.gms:merged',
    'blood_glucose': 'derived:com.google.blood_glucose:com.google.android.gms:merged',
    'activity_minutes': 'derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes',
    'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
    'oxygen_saturation': 'derived:com.google.oxygen_saturation:com.google.android.gms:merged',
    'body_temperature': 'derived:com.google.body.temperature:com.google.android.gms:merged',
    'mensuration':  'derived:com.google.menstruation:com.google.android.gms:merged'
    }

# Function takes in a start date and end date and returns generated synthetic data for each data type
def create_syn_data(start_date,end_date):

    # Create a list of dates between start_date and end_date
    dates = pd.date_range(start_date, end_date)

    # Create empty lists for each data type
    steps = []
    hrs = []
    weight = []
    height = []
    speed = []
    heart_minutes = []
    calories_expended = []
    sleep = []
    blood_pressure = []
    blood_glucose = []
    activity_mins = []
    distance = []
    oxygen_saturation = []
    body_temperature = []
    mensuration = []

    # Create a random device id for the synthetic data
    device_id = ''.join(np.random.choice([*'abcdefghijklmnopqrstuvwxyz0123456789'],8, replace=True))

    # Iterate through each date in the list of dates
    for d in dates:

        # Convert the date to milliseconds
        startmillis = int(d.timestamp()) * 1000
        endmillis = startmillis + 86400000

        # Create a resulting dictionary that we will alter for each data type
        res = {}
        res['startTimeMillis'] = str(startmillis)
        res['endTimeMillis'] = str(endmillis)

        syn_steps = max(0, int(np.random.normal(10000, 9000)))
        avg_syn_hrs = lambda x: np.round(np.random.normal(100,20),14)
        max_syn_hrs = lambda x: np.round(np.random.normal(120,20),14)
        min_syn_hrs = lambda x: np.round(np.random.normal(80,20),14)
        syn_sleep_duration = lambda x: np.round(np.random.normal(8,3),1)
        syn_weight = lambda x: np.round(np.random.normal(70,30),1)
        syn_height = lambda x: np.round(np.random.normal(1.7,0.3),14)
        syn_speed_avg = lambda x: np.round(np.random.normal(2,1),1)
        syn_speed_max = lambda x: np.round(np.random.normal(3,1),1)
        syn_speed_min = lambda x: np.round(np.random.normal(1,0.5),1)
        syn_heart_minutes = lambda x: np.round(np.random.normal(90,30),1)
        syn_calories_expended = lambda x: np.round(np.random.normal(2000,1000),1)
        syn_blood_pressure_sys = lambda x: np.round(np.random.normal(120,20),1)
        syn_blood_pressure_dia = lambda x: np.round(np.random.normal(80,20),1)
        syn_blood_glucose = lambda x: np.round(np.random.normal(100,20),1)
        syn_activity = lambda x: np.round(np.random.normal(100,50))
        syn_distance = lambda x: np.round(np.random.normal(3000,2000),1)
        syn_oxygen_saturation = lambda x: np.round(np.random.normal(96.5,5),1)
        syn_oxygen_flow = lambda x: np.round(np.random.normal(3,2),1)
        syn_body_temperature = lambda x: np.round(np.random.normal(36.5,2),1)
        syn_mensuration = lambda x: np.random.choice([1,2,3,4])


        # Building the resulting dictionary for steps
        res['dataset'] = [{
            'dataSourceId': datasourceids['steps'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.step_count.delta',
                    'originDataSourceId': f'derived:com.google.step_count.delta:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'intVal': syn_steps,
                            'mapVal': []
                        }
                    ]
                }
            ]
        }]
        steps.append(res)

        # Building the resulting dictionary for heart rate
        res['dataset'] = [{
            'dataSourceId': datasourceids['heart_rate'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.heart_rate.bpm',
                    'originDataSourceId': f'derived:com.google.heart_rate.bpm:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': avg_syn_hrs(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': max_syn_hrs(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': min_syn_hrs(0),
                            'mapVal': []
                        }
                    ]
                }
            ]
        }]

        hrs.append(res)

        # Building the resulting dictionary for sleep duration

        res['dataset'] = [{
            'dataSourceId': datasourceids['sleep'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.sleep.segment',
                    'originDataSourceId': f'derived:com.google.sleep.segment:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_sleep_duration(0),
                            'mapVal': []
                        }
                    ]
                }
            ]
        }]
        sleep.append(res)

        # Building the resulting dictionary for weight
        res['dataset'] = [{
            'dataSourceId': datasourceids['weight'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.weight',
                    'originDataSourceId': f'derived:com.google.weight:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_weight(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_weight(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_weight(0),
                            'mapVal': []
                        },
                    ]
                }
            ]
        }]

        weight.append(res)

        # Building the resulting dictionary for height
        res['dataset'] = [{
            'dataSourceId': datasourceids['height'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.height.summary',
                    'originDataSourceId': 'raw:com.google.height:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_height(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_height(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_height(0),
                            'mapVal': []
                        },
                    ]
                }
            ]
        }]

        height.append(res)

        # Building the resulting dictionary for speed
        res['dataset'] = [{
            'dataSourceId': datasourceids['speed'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.speed.summary',
                    'originDataSourceId': f'derived:com.google.speed.summary:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_speed_avg(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_speed_max(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_speed_min(0),
                            'mapVal': []
                        },
                    ]
                }
            ]
        }]
        speed.append(res)

        # Building the resulting dictionary for blood glucose

        res['dataset'] = [{
            'dataSourceId': datasourceids['blood_glucose'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.blood_glucose.summary',
                    'originDataSourceId': 'raw:com.google.blood_glucose:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_blood_glucose(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_glucose(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_glucose(0),
                            'mapVal': []
                        },
                        {'intVal': 2, 'mapVal': []}, {'intVal': 3, 'mapVal': []}, {'mapVal': []}, {'intVal': 2, 'mapVal': []}
                    ]
                }
            ]
        }]

        blood_glucose.append(res)

        # Building the resulting dictionary for blood pressure

        res['dataset'] = [{
            'dataSourceId': datasourceids['blood_pressure'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.blood_pressure.summary',
                    'originDataSourceId': 'raw:com.google.blood_pressure:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_blood_pressure_sys(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_pressure_dia(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_pressure_dia(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_pressure_dia(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_blood_pressure_dia(0),
                            'mapVal': []
                        },
                        {
                            'intVal': 2,
                            'mapVal': []
                        },
                        {
                            'intVal': 2,
                            'mapVal': []
                        }
                    ]
                }
            ]
        }]
        blood_pressure.append(res)

        # Building the resulting dictionary for distance
        res['dataset'] = [{
            'dataSourceId': datasourceids['distance'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.distance.delta',
                    'originDataSourceId': f'derived:com.google.distance.delta:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_distance(0),
                            'mapVal': []
                        },]
                }
            ]
        }]
        distance.append(res)

        # Building the resulting dictionary for heart minutes
        res['dataset'] = [{
            'dataSourceId': datasourceids['heart_minutes'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.heart_minutes.summary',
                    'originDataSourceId': f'derived:com.google.heart_minutes.summary:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_heart_minutes(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_heart_minutes(0),
                            'mapVal': []
                        },]
                }
            ]
        }]
        heart_minutes.append(res)

        # Building the resulting dictionary for calories

        res['dataset'] = [{
            'dataSourceId': datasourceids['calories_expended'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.calories.expended',
                    'originDataSourceId': f'derived:com.google.calories.expended:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_calories_expended(0),
                            'mapVal': []
                        },]
                }
            ]
        }]

        calories_expended.append(res)

        # Building the resulting dictionary for activity_minutes
        res['dataset'] = [{
            'dataSourceId': datasourceids['activity_minutes'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.activity_minutes',
                    'originDataSourceId': f'derived:com.google.activity_minutes.summary:com.google.ios.fit:appleinc.:watch:{device_id}:top_level',
                    'value': [
                        {
                            'fpVal': syn_activity(0),
                            'mapVal': []
                        }]
                }
            ]
        }]

        activity_mins.append(res)

        # Building the resulting dictionary for menstrual cycle

        res['dataset'] = [{
            'dataSourceId': datasourceids['mensuration'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.menstrual_cycle',
                    'originDataSourceId': 'raw:com.google.menstrual_cycle:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_mensuration(0),
                            'mapVal': []
                        }]
                }
            ]
        }]
        mensuration.append(res)

        # Building the resulting dictionary for body temperature

        res['dataset'] = [{
            'dataSourceId': datasourceids['body_temperature'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.body.temperature',
                    'originDataSourceId': 'raw:com.google.body.temperature:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_body_temperature(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_body_temperature(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_body_temperature(0),
                            'mapVal': []
                        }]
                }
            ]
        }]
        body_temperature.append(res)

        # Building the resulting dictionary for oxygen saturation

        res['dataset'] = [{
            'dataSourceId': datasourceids['oxygen_saturation'],
            'point': [
                {
                    'startTimeNanos': str(startmillis * 1000000),
                    'endTimeNanos': str(endmillis * 1000000),
                    'dataTypeName': 'com.google.oxygen_saturation',
                    'originDataSourceId': 'raw:com.google.oxygen_saturation:com.google.android.apps.fitness:user_input',
                    'value': [
                        {
                            'fpVal': syn_oxygen_saturation(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_oxygen_saturation(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_oxygen_saturation(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_oxygen_flow(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_oxygen_flow(0),
                            'mapVal': []
                        },
                        {
                            'fpVal': syn_oxygen_flow(0),
                            'mapVal': []
                        },
                        {
                            'intVal': 1,
                            'mapVal': []
                        },
                        {
                            'intVal': 1,
                            'mapVal': []
                        },
                        {
                            'intVal': 1,
                            'mapVal': []
                        }]
                }
            ]
        }]
        oxygen_saturation.append(res)

    # Retuning the resulting lists
    return steps, hrs, weight, height, speed, heart_minutes, calories_expended, sleep, blood_pressure, blood_glucose, activity_mins, distance, oxygen_saturation, body_temperature, mensuration











