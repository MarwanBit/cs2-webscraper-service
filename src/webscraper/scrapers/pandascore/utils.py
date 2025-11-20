from datetime import datetime, timedelta, timezone
"""
    Preconditions: datetime object is already in UTC
    returns: datetime string in Zulu time, which is what Pandascore uses
"""
def convert_datetime_to_string(date: datetime):
    return date.isoformat().replace('+00:00', 'Z')
