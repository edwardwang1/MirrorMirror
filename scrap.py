from datetime import datetime, date
import pytz
import calendar
tz = pytz.timezone("America/Vancouver")
today = datetime.now(tz)
weekday = calendar.day_name[today.weekday()]
month = calendar.month_name[today.month]
#print(dir(today))
print(today.month)
print(month)
print(today.day)
