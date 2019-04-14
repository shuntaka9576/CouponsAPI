from datetime import datetime


def checkDate(dateString):
    try:
        date = datetime.strptime(dateString, "%Y%m%d")
        return date
    except ValueError:
        return None
