

def get_average(iterable):
    sum_comment_rating = sum([rate.rating for rate in iterable])
    average = round(sum_comment_rating / len(iterable), 1)
    return average