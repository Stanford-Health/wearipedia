import wearipedia
import browsercookie

mfptest = wearipedia.get_device("underarmour/myfitnesspal")




# mfptest.authenticate({})

print(mfptest.get_data("snacks", params={"start_date": "2022-05-16", "end_date": "2022-05-20"}))


