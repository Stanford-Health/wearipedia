import wearipedia

vantage = wearipedia.get_device("polar/vantage")

vantage.authenticate({
    "email":"arjo@stanford.edu",
    "password":"StanfordHealth123"
})

print(len(vantage.get_data("training_by_id", params={"start_date": "2022-08-11", "end_date": "2022-08-11", 'training_id': '7472390363'})))