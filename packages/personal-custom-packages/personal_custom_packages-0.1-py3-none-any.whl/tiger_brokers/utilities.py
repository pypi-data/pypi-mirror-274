from data_extractor import log_function_usage
from datetime import datetime,timezone

'''
    About timestamps:
        UTC
        GMT
            Generally treated as the same.
    
        other time zones has some deivation from UTC/GMT. 

    structure of date time
        24-01-01 12:34:12.789123
            789 -> Millisecond
            123 -> Microsecond
        
'''

def current_UTC_date_time():
    log_function_usage('current_UTC_date_time-tiger_brokers-utilities.py')
    return datetime.now(timezone.utc)

def current_local_date_time():
    log_function_usage('current_local_date_time-tiger_brokers-utilities.py')
    return datetime.now()

def current_local_time():
    log_function_usage('current_local_time-tiger_brokers-utilities.py')
    time = current_local_date_time().strftime('%H:%M:%S')
    time_object = datetime.strptime(time,'%H:%M:%S')
    return time_object

def current_UTC_time():
    log_function_usage('current_UTC_time-tiger_brokers-utilities.py')
    time = current_UTC_date_time().strftime('%H:%M:%S')
    time_object = datetime.strptime(time,'%H:%M:%S')
    return time_object

def timezone_deviation_from_utc():
    log_function_usage('timezone_deviation_from_utc-tiger_brokers-utilities.py')
    return current_local_time() - current_UTC_time()
    
def counting_timestamp_type(timestamp):
    log_function_usage('counting_timestamp_type-tiger_brokers-utilities.py')
    length = len(str(timestamp))
    if(length == 10):
        return f"10 digits: second precision "
    if(length == 13):
        return f"13 digits: millisecond precision"
    if(length == 16):
        return f"16 digits: microsecond precision"

def current_local_timestamp():
    log_function_usage('current_local_timestamp-tiger_brokers-utilities.py')
    return current_local_date_time().timestamp()
    
def current_utc_timestamp():
    log_function_usage('current_utc_timestamp-tiger_brokers-utilities.py')
    return current_UTC_date_time().timestamp()

def create_datetime_object(year, month, day, hour, minute, second, millisecond, microsecond):
    log_function_usage('create_datetime_object-tiger_brokers-utilities.py')
    obj = datetime(year,month,day,hour,minute,second, 000000)
    return obj

def create_datetime_object_v2(date,time):
    log_function_usage('create_datetime_object_v2-tiger_brokers-utilities.py')
    splittedDate = date.split("-")
    splitTime = time.split(":")
    return datetime(int(splittedDate[0]),int(splittedDate[1]),int(splittedDate[2]),int(splitTime[0]),int(splitTime[1]),0,tzinfo=timezone.utc).timestamp()

def timestamp_to_datetime_utc(timestamp):
    log_function_usage('timestamp_to_datetime_utc-tiger_brokers-utilities.py')
    return datetime.utcfromtimestamp(timestamp)

