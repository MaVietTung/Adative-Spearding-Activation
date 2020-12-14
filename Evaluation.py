import json
import Function as function
import numpy as np
import matplotlib.pyplot as plt

with open('data_matrix_smilarities/user_book_with_no_rating_0.json') as fin:
    user_book_grounth_true = json.load(fin)
with open('data_matrix_smilarities/user_book_rating.json') as fin:
    user_book_rating = json.load(fin)
with open('data_matrix_smilarities/book_rate_user.json') as fin:
    book_rate_user = json.load(fin)
with open('data_matrix_smilarities/result_train_smilarites.json') as fin:
    matrix_smilaties = json.load(fin)


def getPredictRate(user, book):
    predict = 0
    if user_book_rating.__contains__(user):
        medium_rating_user = function.getMediumRating(user_book_rating[user])
        if book_rate_user.__contains__(book):
            medium_rating_book = function.getMediumRatingBook(book_rate_user[book])
            K = 0
            S = 0
            for rate in book_rate_user[book]:
                if rate != '0':
                    for user_i in book_rate_user[book][rate]:
                        S += (int(rate) - medium_rating_book) * function.getSimilaritiesValue(user, user_i,
                                                                                              matrix_smilaties)
                        K += 1
            if K != 0:
                predict = medium_rating_user + 1 / K * S
    return predict


user_book_predict = {}
progess = 0
total_progess = len(list(user_book_grounth_true.keys()))
S_error = 0
progess_list = []
progess_MAE_list = []
for user in user_book_grounth_true.keys():
    progess += 1
    print(progess, '/', total_progess)
    S = 0
    for book in user_book_grounth_true[user].keys():
        predict = getPredictRate(user, book)
        if user_book_predict.__contains__(user):
            user_book_predict[user][book] = predict
        else:
            a = {book: predict}
            user_book_predict[user] = a
        S += abs(float(user_book_grounth_true[user][book]) - float(user_book_predict[user][book]))
    S_error += S / len(list(user_book_grounth_true[user].keys()))
    if progess % 1000 == 0:
        progess_list.append(progess)
        progess_MAE_list.append(S_error / progess)

print(progess_MAE_list)
