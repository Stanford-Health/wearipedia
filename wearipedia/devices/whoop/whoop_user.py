import requests


class WhoopUser:
    def __init__(self, email, password):
        self.BASE_URL = "https://api-7.whoop.com/"

        self._login(email, password)
        self.header = {"Authorization": f"bearer {self.token}"}

    def _login(self, email, password):
        """
        Login to whoop API, storing User id and token
        :param email: str email
        :param password: str password
        :return: None will set class variables
        """

        if not email:  # fake the login
            self.token = ""
            self.user_id = ""
        else:
            login = requests.post(
                self.BASE_URL + "oauth/token",
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

    def get_cycles_json(self, params):
        """
        Record base information
        :param params: start, end, other params
        :return: json with all info from cycles endpoint
        """

        params["startTime"] = params["start"]
        params["endTime"] = params["end"]

        del params["start"]
        del params["end"]

        params["apiVersion"] = "7"

        cycles_URL = f"https://api.prod.whoop.com/activities-service/v1/cycles/aggregate/range/{self.user_id}"
        cycles_request = requests.get(cycles_URL, params=params, headers=self.header)

        try:
            data = cycles_request.json()
        except Exception as e:
            exception_str = f"Got exception:\n{e}\n"
            exception_str += f"Received request response is:\n{cycles_request.text}"

            raise Exception(exception_str)

        return data

    def get_heart_rate_json(self, params):
        """
        Get heart rate data on user
        :param params: params for heart rate data
        :return: dict of heart rate data
        """

        params["step"] = "60"
        params["order"] = "t"

        hr_request = requests.get(
            self.BASE_URL + f"users/{self.user_id}/metrics/heart_rate",
            params=params,
            headers=self.header,
        )

        try:
            data = hr_request.json()
        except Exception as e:
            exception_str = f"Got exception:\n{e}\n"
            exception_str += f"Received request response is:\n{hr_request.text}"

            raise Exception(exception_str)

        return data
