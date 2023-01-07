import wearipedia

device = wearipedia.get_device("underarmour/myfitnesspal")

print(device.get_data('exercises_strength',
                      {
                          'start_date': '2022-01-01',
                          'end_date': '2022-05-02'
                      }))
