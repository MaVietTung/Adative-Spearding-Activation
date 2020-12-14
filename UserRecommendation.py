import collections
import json
import Function as function

with open('data_matrix_smilarities/user_book_rating.json') as fin:
    user_book_rating = json.load(fin)
with open('data_matrix_smilarities/book_rate_user.json') as fin:
    book_rate_user = json.load(fin)
with open('data_matrix_smilarities/result_train_smilarites.json') as fin:
    matrix_smilarities = json.load(fin)

user = input()
book_recommendation = []
if user_book_rating.__contains__(user):
    medium_rating = function.getMediumRating(user_book_rating[user])
    if medium_rating == 0:
        book_recommendation = function.getHighRateBook(book_rate_user)
    else:
        book_candidate = function.getBookCandidate(user, user_book_rating, book_rate_user)
        dict_book_predict = {}
        for book in book_candidate:
            if book_rate_user.__contains__(book):
                medium_rating_book = function.getMediumRatingBook(book_rate_user[book])
                S = 0
                K = 0
                if medium_rating_book != 0:
                    for rate in book_rate_user[book].keys():
                        if rate != '0':
                            for user_i in book_rate_user[book][rate]:
                                if user != user_i:
                                    S += (float(rate) - medium_rating_book) * function.getSimilaritiesValue(user, user_i,matrix_smilarities)
                                    K+=1
                    if K!=0:
                        dict_book_predict[book] = medium_rating + 1/K * S
                    else:
                        dict_book_predict[book] = medium_rating
                else:
                    dict_book_predict[book] = medium_rating
        d_sorted_by_value = collections.OrderedDict(sorted(dict_book_predict.items(), key=lambda x: x[1], reverse=True))
        lst = list(d_sorted_by_value.keys())
        if len(lst) >= 20:
            book_recommendation = lst[0:20]
        else:
            book_recommendation = lst

else:
    book_recommendation = function.getHighRateBook(book_rate_user)

print(book_recommendation)
