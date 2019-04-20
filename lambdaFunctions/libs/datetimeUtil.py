from datetime import datetime


def checkDate(dateString):
    """
    /coupons(期間指定問い合せ)時の日付の妥当性をチェックする関数
    """
    try:
        date = datetime.strptime(dateString, "%Y%m%d")
        return date
    except ValueError:
        return None
