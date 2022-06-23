import datetime

def time_at_midnight_yesterday():
    """ return time at midnight yesterday in unix timestamp milliseconds """
    start_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    yesterday_time = start_today - datetime.timedelta(days=1)
    # unix_start_today = int(start_today.timestamp())
    unix_yesterday_time = int(yesterday_time.timestamp())* 1000
    return unix_yesterday_time

def time_at_midnight_today():
    """ return time at midnight today in unix timestamp milliseconds """
    start_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    return int(start_today.timestamp()) * 1000

def time_now():
    """ return time now in unix timestamp milliseconds"""
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    print(yesterday_unix_timestamp)