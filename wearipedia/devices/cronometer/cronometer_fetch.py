import requests
import pandas as pd
import io
import csv


def fetch_real_data(self, start_date, end_date, data_type):
    # This function is called when we want to fetch real data from the
    # device. It is called by the _get_real function in the base class.

    # We need to authenticate first, if we haven't already.
    if self.session is None:
        raise Exception("Not authenticated")

    # Setting the constant urls and headers for the requests

    # The base url for the cronometer app for authentication tokens
    GWTBaseURL = "https://cronometer.com/cronometer/app"

    # Header that refers to the GWT module representing the app version
    GWTHeader = "4487F7F4BACD5C9158608F034F085B7E"

    # The body for the request to get the authentication
    body = f'7|0|5|https://cronometer.com/cronometer/|{GWTHeader}|com.cronometer.shared.rpc.CronometerService|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|-480|'

    # The header for the request to get the authentication
    header = {
        "content-type": "text/x-gwt-rpc; charset=UTF-8",
        'x-gwt-module-base': "https://cronometer.com/cronometer/",
        'x-gwt-permutation': "2D9CD46DC0AA857A2A22311352F8EA94"
    }

    # Making the request to get the authentication
    res = self.session.post(GWTBaseURL, data=body, headers=header)

    if res.status_code != 200:
        raise Exception("Could not fetch the data, authentication failed")

    # The body for the request to get the authentication token
    body = f'7|0|8|https://cronometer.com/cronometer/|{GWTHeader}|com.cronometer.shared.rpc.CronometerService|generateAuthorizationToken|java.lang.String/2004016611|I|com.cronometer.shared.user.AuthScope/2065601159|1fbe8baf50e82dd71832b88d44c1e94c|1|2|3|4|4|5|6|6|7|8|6075068|3600|7|2|'

    # Making the request to get the authentication token
    auth_token = self.session.post(GWTBaseURL, headers=header, data=body)

    if auth_token.status_code != 200:
        raise Exception("Could not fetch the data, authentication failed")

    # cleaning the response to get the token
    auth_token = auth_token.text.split('"')[1]

    # creating the parameters for the get request
    params = {
        'nonce': auth_token,
        'generate': data_type,
        'start': start_date,
        'end': end_date}

    # creating the url for the get request
    data = self.session.get('https://cronometer.com/export', params=params)

    # parsing the data
    content = data.content

    # creating a dataframe from the data
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))

    # returning the dataframe
    return list(df.to_dict('index').values())
