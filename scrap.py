from datetime import datetime
time = "07:00"
d = datetime.strptime(time, "%H:%M")
print(d.strftime("%I:%M %p"))
d = datetime.strptime("00:12", "%H:%M")
print(d.strftime("%I:%M %p"))
