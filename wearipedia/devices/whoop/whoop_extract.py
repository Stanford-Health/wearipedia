from typing import Optional

import re

import pandas as pd
import requests


# Fetch profile
def fetch_profile(access_token: str) -> pd.DataFrame:
    """
    Fetches the basic user profile data from the WHOOP API.

    :param str access_token: The access token for authentication.

    :raises Exception: Raised if the API request fails with a status code other than 200.

    :return: A pandas DataFrame containing the user profile data.
    :rtype: pd.DataFrame
    """
    response = requests.get(
        "https://api.prod.whoop.com/developer/v1/user/profile/basic",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    out = response.json()
    for key in out:
        if not isinstance(out[key], list):
            out[key] = [out[key]]
    df = pd.DataFrame.from_dict(out)
    return df


# Fetch body measurements
def fetch_body_measurements(access_token: str) -> pd.DataFrame:
    """
    Fetches body measurements data from the WHOOP API.

    :param str access_token: The access token for authentication.

    :raises Exception: Raised if the API request fails with a status code other than 200.

    :return: A pandas DataFrame containing body measurements data.
    :rtype: pd.DataFrame
    """
    response = requests.get(
        "https://api.prod.whoop.com/developer/v1/user/measurement/body",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    out = response.json()
    for key in out:
        if not isinstance(out[key], list):
            out[key] = [out[key]]
    df = pd.DataFrame.from_dict(out)

    return df


# Fetch collection
def fetch_collection(
    collection_type: str,
    access_token: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetches collection data from the WHOOP API.

    :param str collection_type: The type of collection to be fetched.
    :param str access_token: The access token for authentication.
    :param str start_date: The start date of the requested data in the format "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS.mmmZ". Defaults to None (not provided).
    :param str end_date: The end date of the requested data in the format "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS.mmmZ". Defaults to None (not provided).

    :raises ValueError: Raised if the provided start_date or end_date is not in the correct format.

    :return: A continuous pandas DataFrame containing all the fetched records.
    :rtype: pd.DataFrame
    """
    long_pattern = re.compile(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}\.\d{3}Z)?")
    short_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    if start_date is not None:  # Check if start_date is given
        # Format dates as required
        if short_pattern.match(start_date):
            start_date = f"{start_date}T00:00:00.000Z"
        elif long_pattern.match(start_date):
            pass
        else:
            raise ValueError(
                "Start date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
            )

    if end_date is not None:  # Check if end_date is given
        # Format dates as required
        if short_pattern.match(end_date):
            end_date = f"{end_date}T00:00:00.000Z"
        elif long_pattern.match(end_date):
            pass
        else:
            raise ValueError(
                "End date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
            )

    next_page = True
    next_token = None

    dfs = []
    while next_page:
        # Make the request
        if collection_type == "Cycle":
            query = "https://api.prod.whoop.com/developer/v1/cycle?limit=20&"
        elif collection_type == "Workout":
            query = "https://api.prod.whoop.com/developer/v1/activity/workout?limit=20&"
        elif collection_type == "Sleep":
            query = "https://api.prod.whoop.com/developer/v1/activity/sleep?limit=20&"
        else:
            raise ValueError(
                'type of collection must either be "Cycle", "Workout", or "Sleep".'
            )
        if start_date is not None:
            query += f"start={start_date}&"
        if end_date is not None:
            query += f"end={end_date}&"
        if next_token is not None:
            query += f"nextToken={next_token}&"
        query = query[:-1]

        response = requests.get(
            query,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        # Process the output
        out = response.json()
        out_next_token, out_records_list = out["next_token"], out["records"]

        record_dict = {
            key: [d[key] for d in out_records_list] for key in out_records_list[0]
        }

        df = pd.DataFrame.from_dict(record_dict)
        dfs.append(df)

        if out_next_token is None:
            next_page = False
            break

        next_token = out_next_token

    result_df = pd.concat(dfs, ignore_index=True)

    return result_df
