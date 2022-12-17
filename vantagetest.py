import wearipedia

vantage = wearipedia.get_device("polar/vantage")

vantage.authenticate({
    "email":"arjo@stanford.edu",
    "password":"StanfordHealth123"
})

print(vantage.get_data("training_history", params={"start_date": "2022-08-18", "end_date": "2022-08-31", 'training_id': '7472390363'}))