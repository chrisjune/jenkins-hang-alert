from datetime import datetime, timezone, timedelta
from dateutil import tz

def convert_millisecond_to_time(millis):
        """
    Millisecond -> readable time
    """
    millis = int(millis)
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def convert_timedelta_to_millisecond(td):
        return (td.days * 86400000) + (td.seconds * 1000) + (td.microseconds / 1000) 

def convert_timestamp_to_datetime(timestamp):
        """
    Unix timestamp -> datetime
    """
    timestamp /= 1000
    date_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=tz.gettz('Asia/Seoul'))
    return date_time
