import datetime
from main import settings
def get_avg(iterable: list):
    sum_comment_rating = sum(iterable)
    average = round(sum_comment_rating / len(iterable), 1)
    return average


def get_count(iterable: list):
    count = 0
    for item in iterable:
        if item.is_active == True:
            count += 1
    return count

def get_discount(price, discount):
    discount = price * discount // 100
    return price - discount


def get_average(iterable):
    sum_comment_rating = sum([rate.rating for rate in iterable])
    average = round(sum_comment_rating / len(iterable), 1)
    return average


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )
