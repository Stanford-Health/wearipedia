
import wearipedia

gfit = wearipedia.get_device("google/googlefit")

gfit.authenticate({
"access_token": 'ya29.a0AeTM1ifHumwAF5JVUkdFmcSPTl08bAX7TNj6AOy6nRJ0vcgBZ-HXjohl_555He9IHesvfjnCFRjRY9igpnbCtk9Z3DR-51xHpgrDohPE37FdV6iMFPULJRCWKytFz1WA9NPs2qGvQC3-xLfaOAgcSQrW_NVYaCgYKARISARESFQHWtWOmbIhploefjEEb4QKEV4LTJw0163'
})

print(gfit.get_data("steps", params={"start_date": "2022-05-16", "end_date": "2022-06-16"}))

garmin = wearipedia.get_device("garmin/fenix_7s")

print(garmin.get_data("steps")[0][0])
