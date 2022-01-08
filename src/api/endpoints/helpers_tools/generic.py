import datetime


def get_today_str() -> str:
    return datetime.datetime.utcnow().strftime("%Y%m%d")
