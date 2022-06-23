import datetime

def time_at_start_yesterday():
    """ return time at 00:00:00 yesterday in unix timestamp milliseconds """
    start_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    yesterday_time = start_today - datetime.timedelta(days=1)
    unix_yesterday_time = int(yesterday_time.timestamp())* 1000
    return unix_yesterday_time

def time_at_start_today():
    """ return time at 00:00:00 today in unix timestamp milliseconds """
    start_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    return int(start_today.timestamp()) * 1000

def time_now():
    """ return time now in unix timestamp milliseconds"""
    now = datetime.datetime.now()
    unix_now = int(now.timestamp()) * 1000
    print(unix_now)