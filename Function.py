import collections


def getSimilaritiesValue(user1, user2, matrix_similarities):
    if user1 == user2:
        return 1
    if matrix_similarities.__contains__(user1):
        if matrix_similarities[user1].__contains__(user2):
            return float(matrix_similarities[user1][user2])
    if matrix_similarities.__contains__(user2):
        if matrix_similarities[user2].__contains__(user1):
            return float(matrix_similarities[user2][user1])
    return 0


def getMediumRating(book_rating):
    total = 0
    total_rating = 0
    for book in book_rating.keys():
        if book_rating[book] != '0':
            total += 1
            total_rating += int(book_rating[book])
    if total != 0:
        return total_rating / total
    else:
        return 0


def getBookCandidate(user, user_book_rate, book_rate_user):
    book_candidate = []
    user_smilarities = []
    for book in user_book_rate[user].keys():
        if book_rate_user.__contains__(book):
            for rate in book_rate_user[book].keys():
                if rate != '0':
                    user_smilarities = user_smilarities + book_rate_user[book][rate]
    if user_smilarities.__contains__(user):
        user_smilarities.remove(user)
    for user_i in user_smilarities:
        if user_book_rate.__contains__(user_i):
            book_candidate = book_candidate + list(user_book_rate[user_i].keys())
    for book in user_book_rate[user].keys():
        if book_candidate.__contains__(book):
            book_candidate.remove(book)
    return book_candidate


def getHighRateBook(book_rate_user):
    rating = 0
    total = 0
    dictionary = {}
    for book in book_rate_user:
        for rate in book_rate_user[book]:
            if rate != '0':
                rating += int(rate) * len(list(book_rate_user[book][rate]))
                total += len(list(book_rate_user[book][rate]))
                dictionary[book] = rating / total
    d_sorted_by_value = collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
    lst = list(d_sorted_by_value.keys())
    if len(lst) >= 20:
        return lst[0:20]
    else:
        return lst


def getMediumRatingBook(rate_user):
    rating = 0
    rate_total = 0
    for rate in rate_user:
        if rate != '0':
            rating += int(rate)
            rate_total += len(rate_user[rate])
    if rate_total != 0:
        return rating / rate_total
    else:
        return 0
