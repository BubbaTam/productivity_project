import os
import datetime
import json

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

def save_json_file(data_variable,folder_location, file_name:str,):
    json_file = json.dumps(data_variable)
    path_file = os.path.join(folder_location, file_name +".json")
    with open(path_file,'w') as f:
        f.write(json_file)

def dummy_sql_statement():
    return "select 2+2;"

def ISO_8601_to_unix_timestamp_milliseconds(time:str, time_format:str)-> str:
    """
    Return the conversion of a time string to unix timestamp milliseconds

    Examples time format strings:

    2022-11-09T09:55:19+00:00 == "%Y-%m-%dT%H:%M:%S%z"

    2022-11-09 == "%Y-%m-%d"
    """
    datetime_object = datetime.datetime.strptime(time, time_format)
    time = int(datetime_object.timestamp()) *1000
    return time