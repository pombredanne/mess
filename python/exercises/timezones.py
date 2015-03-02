from datetime import datetime
import pytz
import random

ZONES = []

for _ in range(6):
    ZONES.append(pytz.timezone(random.choice(pytz.all_timezones)))


fmt = '%Y-%m-%d %H:%M %Z%z'

while True:
    date_input = input("When? MM/DD/YYYY HH:MM >> ")
    try:
        local_date = datetime.strptime(date_input, '%m/%d/%Y %H:%M')

    except ValueError:
        print("{} is not a valid time...".format(date_input))

    else:
        local_date = pytz.timezone('Africa/Johannesburg').localize(local_date)
        utc_date = local_date.astimezone(pytz.utc)

        output = []
        for timezone in ZONES:
            output.append(utc_date.astimezone(timezone))
        print(output)

        for appointment in output:
            print(appointment.strftime(fmt))
        break
