a="Fri Jan 01 08:30:03 +0800 2021"

import datetime
time_format=datetime.datetime.strptime(a,'%a %b %d %H:%M:%S %z %Y')
time_format=str(time_format)
print(time_format)
times=time_format[0:10]
print(times)

if times=="2021-01-01":
	print("yes")
else:
	print("no")