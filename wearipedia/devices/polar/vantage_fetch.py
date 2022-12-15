import requests
import re
import pandas as pd
import io

def fetch_real_data(self, start_date, end_date, data_type, training_id=None):
    json_data = {
            'userId': self.USERID,
            'fromDate': start_date,
            'toDate': end_date,
        }

    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }

    payload = {
        "email": self.email,
        "password":self.password,
    }

    if self.session == None:
        with requests.Session() as session:

            post = session.post('https://flow.polar.com/login', data=payload)

            #using regular expressions, we can search for the userId in the session response 
            result = re.search('AppGlobal.init((.*))', post.text)
            
            # if the userId is not found, the login failed
            if result == None:
                print('Not Authenticated')
                return
        self.session = session

    #get the actual training session data
    if data_type == "training_history":
        activities = self.session.post('https://flow.polar.com/api/training/history', cookies=self.session.cookies.get_dict(), headers=headers, json=json_data)
        if activities.status_code!=200:
            print('Activity data not found')
            return []
        activities = activities.json()
        return activities
    if data_type == 'sleep':
        sleep_req_link = f'https://sleep-api.flow.polar.com/api/sleep/report?from={start_date}&to={end_date}'
        sleep = self.session.get(sleep_req_link, cookies=self.session.cookies.get_dict(), headers=headers, json=json_data)
        if sleep.status_code!=200:
            print('Sleep data not found')
            return []
        return sleep.json()
    if data_type == 'training_by_id':
        if training_id == None:
            print('Please provide training_id')
            return []
        r = self.session.get('https://flow.polar.com/api/export/training/csv/'+training_id)
        if r.status_code!=200:
            print('Training data not found')
            return []
        res_df = pd.read_csv(io.StringIO(r.text), sep=',', engine='python')

        filtered = res_df.to_dict('index')

        arr = []

        for i in filtered:
            arr.append(filtered[i])

        return arr


