
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



