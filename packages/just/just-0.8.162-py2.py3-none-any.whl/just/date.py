from datetime import datetime, timedelta


def yesterday(days_extra=0):
    return datetime.now() - timedelta(days=1 + days_extra)
