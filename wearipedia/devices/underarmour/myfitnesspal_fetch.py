import pandas as pd

def fetch_real_data(self,start_date, end_date, data_type):

    if self.client == None:
        print('Not Authenticated, login and try again')
    
    days = pd.date_range(start_date, end_date, freq='D')

    if data_type == 'goals':
        goals = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).goals
            res['date'] = day
            goals.append(res)
        return goals
    if data_type == 'daily_summary':
        summary = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).totals
            res['date'] = day
            summary.append(res)
        return summary
    if data_type == 'exercises_cardio':
        cardio = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).exercises[0].get_as_list()
            res = [{'day':day}]+res
            cardio.append(res)
        return cardio
    if data_type == 'exercises_strength':
        strength = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).exercises[1].get_as_list()
            res = [{'day':day}]+res
            strength.append(res)
        return strength
    if data_type == 'breakfast':
        breakfast = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[0].get_as_list()
            if len(res) == 0:
                res.append({'date':day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[0].totals
            breakfast.append(res)
        return breakfast
    if data_type == 'lunch':
        lunch = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[1].get_as_list()
            if len(res) == 0:
                res.append({'date':day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[1].totals
            lunch.append(res)
        return lunch
    if data_type == 'dinner':
        dinner = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[2].get_as_list()
            if len(res) == 0:
                res.append({'date':day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[2].totals
            dinner.append(res)
        return dinner
    if data_type == 'snacks':
        snacks = []
        for day in days:
            res = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[3].get_as_list()
            if len(res) == 0:
                res.append({'date':day})
            else:
                res[0]['date'] = day
                res[0]['totals'] = self.client.get_date(int(day.year),int(day.month),int(day.day)).meals[3].totals
            snacks.append(res)
        return snacks

    

