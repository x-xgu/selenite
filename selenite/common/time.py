import datetime
import itertools
import time

DATETIME_FULL = '%Y-%m-%d %H:%M:%S'
DATETIME_SHORT = '%Y-%m-%d %H:%M'
DATETIME_DATE = '%Y-%m-%d'
DATETIME_TIME = '%H:%M:%S'
UTC_DATETIME = '%Y-%m-%dT%H:%M:%S.000Z'


def get_timestamp(

) -> int:
    """
    Get current timestamp
    """
    return int(datetime.datetime.timestamp(datetime.datetime.now()))


def get_utc_datetime(

) -> datetime.datetime:
    """
    Get current UTC datetime
    """
    return datetime.datetime.utcnow()


def format_datetime(
        dt: datetime.datetime,
        time_format: str
) -> str:
    """
    Format datetime to string
    """
    return dt.strftime(time_format)


def get_current_date(

) -> str:
    """
    Get current date
    """
    return datetime.datetime.now().date().isoformat()


def get_current_time(

) -> str:
    """
    Get current time
    """
    return datetime.datetime.now().strftime(DATETIME_FULL)


def add_days(
        days: int,
        base_time: str = None
) -> str:
    """
    Add days to base time
    """
    base_time = get_current_date() if not base_time else base_time
    date = datetime.datetime.fromisoformat(base_time)
    new_date = date + datetime.timedelta(days=days)
    return new_date.date().isoformat()


def add_hours_and_days(
        hours: int,
        days: int,
        base_time: str = None
) -> str:
    """
    Add hours and days to base time
    """
    base_time = get_current_time() if not base_time else base_time
    dt = datetime.datetime.strptime(base_time, DATETIME_FULL)
    new_dt = dt + datetime.timedelta(hours=hours, days=days)
    return new_dt.strftime(DATETIME_FULL)


def wait(
        seconds: float,
        show_with_terminal: bool = False
) -> None:
    """
    Wait for seconds
    """
    if not show_with_terminal:
        time.sleep(seconds)
    else:
        iteration = 0
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        while iteration < seconds:
            progress = int(iteration / seconds * 20)
            bar = '=' * progress + '-' * (20 - progress)
            percent = (iteration / seconds) * 100
            print('\rWaiting {}s {} [{}] {:.0f}%'.format(seconds, next(spinner), bar, percent), end='')
            time.sleep(0.25)
            iteration += 0.25
        print('\rDone!')
