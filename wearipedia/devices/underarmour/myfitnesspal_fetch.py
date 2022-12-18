import pandas as pd

# This is the class that will be used to fetch data from MyFitnessPal


def fetch_real_data(self, start_date, end_date, data_type):

    # if the client is not set, we need to login
    if self.client == None:
        print('Not Authenticated, login and try again')

    # creating the date range from the start and end dates
    days = pd.date_range(start_date, end_date, freq='D')

    # if the data type is goals, we need to get the goals for each day using the client
    if data_type == 'goals':
        # creating an empty list to store the goals
        goals = []

        # for each day in the date range, we get the goals for that day
        for day in days:
            # using the client, we get the goals for the day
            res = self.client.get_date(
                int(day.year), int(day.month), int(day.day)).goals
            # we add the date to the goals
            res['date'] = day
            # we append the goals to the list
            goals.append(res)
        # we return the list of goals
        return goals

    # if the data type is daily_summary, we need to get the daily summary for each day using the client
    if data_type == 'daily_summary':
        # creating an empty list to store the daily summary
        summary = []

        # for each day in the date range, we get the daily summary for that day
        for day in days:
            # using the client, we get the daily summary for the day
            res = self.client.get_date(
                int(day.year), int(day.month), int(day.day)).totals
            # we add the date to the daily summary
            res['date'] = day
            # we append the daily summary to the list
            summary.append(res)

        # we return the list of daily summary
        return summary

    # if the data type is exercises_cardio, we need to get the cardio exercises for each day using the client
    if data_type == 'exercises_cardio':

        # creating an empty list to store the cardio exercises
        cardio = []

        # for each day in the date range, we get the cardio exercises for that day
        for day in days:
            # using the client, we get the cardio exercises for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).exercises[0].get_as_list()
            # we add the date to the cardio exercises
            res = [{'day': day}]+res
            # we append the cardio exercises to the list
            cardio.append(res)
        # we return the list of cardio exercises
        return cardio

    # if the data type is exercises_strength, we need to get the strength exercises for each day using the client
    if data_type == 'exercises_strength':

        # creating an empty list to store the strength exercises
        strength = []

        # for each day in the date range, we get the strength exercises for that day
        for day in days:
            # using the client, we get the strength exercises for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).exercises[1].get_as_list()
            # we add the date to the strength exercises
            res = [{'day': day}]+res
            # we append the strength exercises to the list
            strength.append(res)
        # we return the list of strength exercises
        return strength

    # if the data type is breakfast, we need to get the other exercises for each day using the client
    if data_type == 'breakfast':

        # creating an empty list to store the breakfast foods
        breakfast = []

        # for each day in the date range, we get the breakfast foods for that day
        for day in days:

            # using the client, we get the breakfast foods for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).meals[0].get_as_list()

            # if the length of the list is 0, skip the totals
            if len(res) == 0:
                res.append({'date': day})

            # if the length of the list is not 0, we add the date and the totals to the list
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(
                    int(day.year), int(day.month), int(day.day)).meals[0].totals

            # we append the breakfast foods to the list
            breakfast.append(res)

        # we return the list of breakfast foods
        return breakfast

    # if the data type is lunch, we need to get the lunch foods for each day using the client
    if data_type == 'lunch':

        # creating an empty list to store the lunch foods
        lunch = []
        # for each day in the date range, we get the lunch foods for that day using the client
        for day in days:

            # using the client, we get the lunch foods for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).meals[1].get_as_list()

            # if the length of the list is 0, skip the totals
            if len(res) == 0:
                res.append({'date': day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(
                    int(day.year), int(day.month), int(day.day)).meals[1].totals

            # we append the lunch foods to the list
            lunch.append(res)

        # we return the list of lunch foods
        return lunch

    # if the data type is dinner, we need to get the dinner foods for each day using the client
    if data_type == 'dinner':

        # creating an empty list to store the dinner foods
        dinner = []

        # for each day in the date range, we get the dinner foods for that day using the client
        for day in days:

            # using the client, we get the dinner foods for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).meals[2].get_as_list()

            # if the length of the list is 0, skip the totals
            if len(res) == 0:
                res.append({'date': day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(
                    int(day.year), int(day.month), int(day.day)).meals[2].totals

            # we append the dinner foods to the list
            dinner.append(res)
        # we return the list of dinner foods
        return dinner

    # if the data type is snacks, we need to get the snacks for each day using the client
    if data_type == 'snacks':

        # creating an empty list to store the snacks
        snacks = []

        # for each day in the date range, we get the snacks for that day using the client
        for day in days:

            # using the client, we get the snacks for the day
            res = self.client.get_date(int(day.year), int(
                day.month), int(day.day)).meals[3].get_as_list()

            # if the length of the list is 0, skip the totals
            if len(res) == 0:
                res.append({'date': day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(
                    int(day.year), int(day.month), int(day.day)).meals[3].totals

            # we append the snacks to the list
            snacks.append(res)
        # we return the list of snacks
        return snacks
