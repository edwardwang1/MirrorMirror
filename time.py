#!/usr/bin/env python
import datetime
import pytz


tz = pytz.timezone("America/Vancouver")
today = datetime.datetime.now(tz)
midnightPrev = today.replace(hour = 00, minute = 00, second = 00, microsecond = 000000)
midnightPrev = midnightPrev.astimezone(pytz.timezone("utc")).isoformat()
midnightNext = today.replace(hour = 23, minute = 59, second = 59, microsecond = 999999)
midnightNext = midnightNext.astimezone(pytz.timezone("utc")).isoformat()
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
midnightPrev2 = midnightPrev[:-6] + 'Z'
midnightNext2 = midnightNext[:-6] + 'Z'
print(now)
print(midnightPrev2)
print(midnightNext2)

'''
tz = pytz.timezone("America/Vancouver")
# 1. get correct date for the midnight using given timezone.
today = datetime.datetime.now(tz)
#today = datetime.datetime.now()
print(today)
midnightPrev = today.replace(hour = 00, minute = 00, second = 00, microsecond = 000000)
midnightNext = today.replace(hour = 23, minute = 59, second = 59, microsecond = 999999)
print(midnightNext)
print(today.isoformat())
print(type(today))
print(today.tzinfo)
print(midnightPrev.astimezone(pytz.timezone("utc")))
'''


