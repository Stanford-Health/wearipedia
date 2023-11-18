import numpy as np

def generate_synthetic_heart_rate_data(size=np.random.randint(60,1800), min_hr=60, max_hr=160):
        heart_rate_data = {'heartrate': {'data': [], 'series_type': 'time', 'original_size': size, 'resolution': 'high'},
                        'time': {'data': list(range(size)), 'series_type': 'time', 'original_size': size, 'resolution': 'high'}}
        
        for _ in range(size):
            heart_rate_data['heartrate']['data'].append(np.random.randint(min_hr, max_hr))

        return [heart_rate_data]

def return_streams_syn(data_type):
      if data_type == 'heartrate':
        return generate_synthetic_heart_rate_data()