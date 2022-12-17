
import wearipedia

gfit = wearipedia.get_device("google/googlefit")

# gfit.authenticate({
# "access_token": 'ya29.a0AX9GBdXaNyTiM9YmEXioeS-tUAN32dQpG-VG3dRAWeJhZTIbPAm2qtEVBf3q-HSEpslo7MiNQUqs37BJ5PUCK5iVzkyjkurdhWGA_OcfypXzrQSU5AHwfT6vG2a3ap1UcpsDOEiws9xPmLii96ZsWqD_3ocDaCgYKAYISARESFQHUCsbCaIJ2jbngr-oJW3yWy0UXAw0163'})

for x in ['steps','heart_rate', 'sleep', 'heart_minutes','blood_pressure', 'blood_glucose', 'body_temperature', 'calories_expended', 'activity_minutes', 'height', 'oxygen_saturation', 'mensuration', 'speed', 'weight','distance']:
    print(gfit.get_data(x, params={"start_date": "2022-05-10", "end_date": "2022-05-17"}))

# garmin = wearipedia.get_device("garmin/fenix_7s")

# print(garmin.get_data("steps")[0][0])
