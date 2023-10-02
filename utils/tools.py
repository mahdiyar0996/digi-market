
def get_avg(iterable: list):
    sum_comment_rating = sum(iterable)
    average = round(sum_comment_rating / len(iterable), 1)
    return average

def get_count(iterable: list):
    count = 0
    for item in iterable:
        count += 1
    return  count

def get_average(iterable):
    sum_comment_rating = sum([rate.rating for rate in iterable])
    average = round(sum_comment_rating / len(iterable), 1)
    return average