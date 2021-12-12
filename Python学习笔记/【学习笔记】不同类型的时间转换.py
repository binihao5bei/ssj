from datetime import datetime
from datetime import date,timedelta
creat_time="昨天10点"
if "刚刚" in creat_time:
    time=datetime.now().strftime("%Y-%m-%d")
    print(time)
elif "小时" in creat_time:
    hour=creat_time[:creat_time.find("小时")]
    hour=timedelta(hours=int(hour))
    time=(datetime.now()-hour).strftime("%Y-%m-%d")
    print(time)
elif "分钟" in creat_time:
    minute=creat_time[:creat_time.find("分钟")]
    minute=timedelta(hours=int(minute))
    time=(datetime.now()-minute).strftime("%Y-%m-%d")
    print(time)
elif "昨天" in creat_time:
    today=datetime.now()
    detday=timedelta(days=1)
    da_days=today-detday
    time=da_days.strftime("%Y-%m-%d")
else:
    time_format=datetime.datetime.strptime(creat_time,'%a %b %d %H:%M:%S %z %Y')   #带时区时间转化
    time_format=str(time_format)
    time=time_format[0:10]
    print(time)

    print(time)
