import requests


def fetch_real_data(start_date, end_date, data_type, headers):
    """Main function for fetching real data from the nutrisense database.
    Uses Nutrisense's internal API.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "continiuous", "summary", "scores", "statistics"
    :type data_type: str
    :param headers: current header with credentials to Nutrisense, pre authenticated
    :type headers: requests.sessions.Session
    :return: the data fetched from the API according to the inputs
    :rtype: list[dict] (for continuous data) or dict (otherwise)
    """

    if data_type == "continuous" or data_type == "summary":
        json_data = {
            "operationName": "allCharts",
            "variables": {
                "filter": {
                    "types": [
                        {
                            "key": "timeline",
                            "value": [],
                        },
                    ],
                    "startDate": start_date,
                    "endDate": end_date,
                },
            },
            "query": "query allCharts($filter: DateFilter) {\n  allCharts(filter: $filter) {\n    charts {\n      type\n      title\n      description\n      xAxis\n      yAxis\n      range {\n        min\n        max\n        goal\n        goalMin\n        goalMax\n        __typename\n      }\n      meta {\n        key\n        tag\n        section\n        __typename\n      }\n      values {\n        ... on TimePair {\n          x\n          y\n          interpolated\n          __typename\n        }\n        ... on NumericPair {\n          x\n          y\n          __typename\n        }\n        ... on StringPair {\n          name\n          x\n          y\n          __typename\n        }\n        ... on RangePair {\n          x {\n            min\n            max\n            __typename\n          }\n          y\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
        }

        response = requests.post(
            "https://api-production.nutrisense.io/graphql",
            headers=headers,
            json=json_data,
            verify=False,
        )
        res = response.json()

        if data_type == "continuous":
            return res["data"]["allCharts"]["charts"][0]["values"]
        elif data_type == "summary":
            return res["data"]["allCharts"]["charts"][0]["range"]

    else:
        json_data = {
            "operationName": "allNutrition",
            "variables": {
                "filter": {
                    "startDate": start_date,
                    "endDate": end_date,
                },
            },
            "query": "query allNutrition($filter: DateFilter) {\n  allNutrition(filter: $filter) {\n    nutrition {\n      today {\n        key\n        value\n        __typename\n      }\n      average {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    score {\n      today {\n        scoreTimeOutsideRange\n        scorePeak\n        scoreMean\n        scoreStdDev\n        score\n        __typename\n      }\n      __typename\n    }\n    statistics {\n      today {\n        healthyRange {\n          min\n          max\n          __typename\n        }\n        range {\n          min\n          max\n          __typename\n        }\n        timeWithinRange\n        min\n        max\n        mean\n        median\n        standardDeviation\n        q1\n        q3\n        score\n        __typename\n      }\n      average {\n        healthyRange {\n          min\n          max\n          __typename\n        }\n        range {\n          min\n          max\n          __typename\n        }\n        timeWithinRange\n        min\n        max\n        mean\n        median\n        standardDeviation\n        q1\n        q3\n        score\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
        }

        response = requests.post(
            "https://api-production.nutrisense.io/graphql",
            headers=headers,
            json=json_data,
            verify=False,
        )
        res = response.json()

        if data_type == "scores":
            return res["data"]["allNutrition"]["score"]["today"]
        elif data_type == "statistics":
            return {
                "today": res["data"]["allNutrition"]["statistics"]["today"],
                "average": res["data"]["allNutrition"]["statistics"]["average"],
            }
