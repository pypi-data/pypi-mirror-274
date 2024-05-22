from datetime import datetime, timezone


def get_current_datetime() -> datetime:
    return datetime.now(tz=timezone.utc)


def get_current_timestamp_ms() -> int:
    now = get_current_datetime()
    return int(datetime.timestamp(now) * 1000)


def get_datetime_from_timestamp_ms(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)


def get_timestamp_ms_from_datetime(dt: datetime) -> int:
    return int(datetime.timestamp(dt) * 1000)
