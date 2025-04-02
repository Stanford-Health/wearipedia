import io
import re

import pandas as pd
import requests

# This is the class that will be used to fetch data from Polar Flow


def fetch_real_data(
    access_token, user_id, start_date, end_date, data_type, training_id=None
):
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}

    if data_type == "training_data":
        training_history = []
        r = requests.post(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions",
            headers=headers,
        )

        if r.status_code == 201:
            transaction_id = r.json()["transaction-id"]
        elif r.status_code == 204:
            print("No data available")
            return []
        else:
            raise Exception("Opening transaction for training history failed:", r)

        r = requests.get(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions/{transaction_id}",
            headers=headers,
        )

        if r.status_code >= 200 and r.status_code < 400:
            training_history = r.json()["exercises"]
        else:
            raise Exception("Failed to fetch exercises:", r)

        r = requests.put(
            "https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions/{transaction_id}",
            headers=headers,
        )
        return training_history

    # get the sleep data
    elif data_type == "sleep":

        r = requests.get(
            "https://www.polaraccesslink.com/v3/users/sleep", headers=headers
        )

        if r.status_code >= 200 and r.status_code < 400:
            return r.json()["nights"]
        else:
            raise Exception("Failed to fetch sleep data:", r)

    # get the training data by id
    elif data_type == "training_by_id":
        if not training_id:
            raise Exception("No training_id specified")
        training_data = {}
        r = requests.post(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions",
            headers=headers,
        )

        if r.status_code == 201:
            transaction_id = r.json()["transaction-id"]
        elif r.status_code == 204:
            print("No data available")
            return {}
        else:
            raise Exception("Opening transaction for training history failed:", r)

        r = requests.get(
            "https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions/{transaction_id}/exercises/{training_id}",
            headers=headers,
        )

        if r.status_code >= 200 and r.status_code < 400:
            training_data = r.json()
        else:
            raise Exception("Failed to fetch exercises:", r)

        r = requests.put(
            "https://www.polaraccesslink.com/v3/users/{user_id}/exercise-transactions/{transaction_id}",
            headers=headers,
        )
        return training_data
    elif data_type == "daily_activity":
        daily_activity = []
        r = requests.post(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions",
            headers=headers,
        )

        if r.status_code == 201:
            transaction_id = r.json()["transaction-id"]
        elif r.status_code == 204:
            print("No data available")
            return []
        else:
            raise Exception("Opening transaction for activity history failed:", r)

        r = requests.get(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions/{transaction_id}",
            headers=headers,
        )

        if r.status_code >= 200 and r.status_code < 400:
            training_history = r.json()["activity-log"]
        else:
            raise Exception("Failed to fetch activities:", r)

        r = requests.put(
            "https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions/{transaction_id}",
            headers=headers,
        )
        return training_history
    elif data_type == "activity_by_id":
        if not training_id:
            raise Exception("No training_id specified")
        training_data = {}
        r = requests.post(
            f"https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions",
            headers=headers,
        )

        if r.status_code >= 200 and r.status_code < 400:
            transaction_id = r.json()["transaction-id"]
        else:
            raise Exception("Opening transaction for training history failed:", r)
        r = requests.get(
            "https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions/{transaction_id}/activities/{training_id}",
            headers=headers,
        )

        if r.status_code >= 200 and r.status_code < 400:
            training_data = r.json()
        else:
            raise Exception("Failed to fetch activity:", r)

        r = requests.put(
            "https://www.polaraccesslink.com/v3/users/{user_id}/activity-transactions/{transaction_id}",
            headers=headers,
        )
        return training_data
    else:
        raise Exception("Unhandled data type requested")
