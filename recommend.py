import os
import math
import json
import random
import collections

from tqdm import notebook, tqdm

from utils.functions import Function
from utils.utils import precision_recall, f1_score, rankscore, avg_precision
from config import *


class Recommender:
    def __init__(self, path, rate_max, is_trained=True):
        with open(os.path.join(path, 'user_book_rating.json')) as fin:
            self.user_book_rating = json.load(fin)

        with open(os.path.join(path, 'book_rate_user.json')) as fin:
            self.book_rate_user = json.load(fin)

        with open(os.path.join(path, 'book_user_rating.json')) as fin:
            self.book_user_rate = json.load(fin)

        if is_trained:
            with open(os.path.join(path, 'result_train_similarities.json')) as fin:
                self.matrix_similarities = json.load(fin)
        else:
            with open(os.path.join(path, 'matrix_similarities.json')) as fin:
                self.matrix_similarities = json.load(fin)

        self.functions = Function(self.user_book_rating, self.book_rate_user, self.matrix_similarities, self.book_user_rate)

        self.epochs = epochs
        self.n_preds = n_preds
        self.rate_max = rate_max

    def RMS(self, item_i, rating_x, rating_y):
        R_x_i = self.book_rate_user[item_i][rating_x]
        R_y_i = self.book_rate_user[item_i][rating_y]

        w = 1 / len(R_x_i) * 1 / len(R_y_i)
        total = 0
        for user_s in R_x_i:
            for user_t in R_y_i:
                total += self.functions.getSimilaritiesValue(user_s, user_t)
        result = total * w
        return result

    def calculate(self, user_a, user_i):
        similarities = 0
        len_item = 0
        for item in self.user_book_rating[user_a].keys():
            if self.user_book_rating[user_i].__contains__(item):
                if self.user_book_rating[user_a][item] != self.user_book_rating[user_i][item]:
                    similarities += self.RMS(item, self.user_book_rating[user_a][item], self.user_book_rating[user_i][item])
                    len_item += 1
        if len_item != 0:
            return similarities / len_item
        else:
            return 0

    def train(self):
        print('============= Training RSM =============')

        # with open('data_matrix_similarities/progress.txt', 'r') as fin:
        #     progress = fin.readline()
        #     epochs = fin.readline()
        # progress = int(progress)
        # epochs = int(epochs)
        # print('continue train for progress and epoch:', progress, epochs)

        # if (progress != 0) | (epochs != 0):
        #     with open('data_matrix_similarities/result_train_similarities.json') as fin:
        #         self.matrix_similarities = json.load(fin)

        # total_progress = len(self.matrix_similarities.keys())
        active_list = list(self.matrix_similarities.keys())

        for epoch in range(self.epochs):
            print('Epoch: {:} / {:}'.format(epoch + 1, self.epochs + 1))
            for active_user in tqdm(active_list):
                # progress += 1
                # print(progress, '/', total_progress)

                # if progress % 100 == 0:
                #     with open('data_matrix_similarities/result_train_similarities.json', 'w') as fout:
                #         json.dump(self.matrix_similarities, fout)
                #     with open('data_matrix_similarities/progress.txt', 'w') as fout:
                #         fout.write(str(progress) + '\n')
                #         fout.write(str(epoch) + '\n')
                #     # print('saved\n')

                for user_i in self.matrix_similarities[active_user].keys():
                    if active_user != user_i:
                        t = self.calculate(active_user, user_i)
                        if t != 0:
                            self.matrix_similarities[active_user][user_i] = t

        with open('data_matrix_similarities/result_train_similarities.json', 'w') as fout:
            json.dump(self.matrix_similarities, fout)

    def predict_rate(self, user, book, enable_print=True, threshold=0.3, cnt_threshold=2):
        predict = None
        if self.user_book_rating.__contains__(user):
            user_rates = self.user_book_rating[user]
            if user_rates.__contains__(book):
                if enable_print:
                    print("User has already rated this book. ")
                return int(user_rates[book])
            medium_rating_user = self.functions.getMediumRating(user)
            if self.book_rate_user.__contains__(book):
                K = 0
                S = 0
                cnt = 0
                for rate in self.book_rate_user[book]:
                    if rate != '0':
                        for user_i in self.book_rate_user[book][rate]:
                            w = self.functions.getSimilaritiesValue(user, user_i)

                            # Only consider users with similarity greater than a threshold
                            if w < threshold:
                                continue

                            S += (int(rate) - self.functions.getMediumRating(user_i)) * w
                            K += w
                            cnt += 1

                            if enable_print:
                                print('{user}:\t{rate},\t{avg_rate} - {similarity}'.format(user=user_i, rate=rate, avg_rate=round(self.functions.getMediumRating(user_i), 2), similarity=w))

                if K != 0 and cnt > cnt_threshold:
                    predict = medium_rating_user + 1 / K * S
                    if predict > self.rate_max:
                        predict = self.rate_max
                    elif predict < 1:
                        predict = 1
        elif enable_print:
            print("User has too few ratings to predict. ")

        return predict

    def prediction(self, user, n_pred=20, enable_print=True):
        book_recommendation = []

        if self.user_book_rating.__contains__(user):
            medium_rating = self.functions.getMediumRating(user)
            # print("User avg rating: ", medium_rating)

            # if medium_rating == 0:
            #     if enable_print:
            #         print("User does not have any explicit ratings.")
            #     book_recommendation = self.functions.getHighRateBook()
            #
            # else:

            book_candidate = self.functions.getBookCandidate(user)
            # book_candidate = self.book_rate_user.keys()

            if enable_print:
                print("Book Candidate: ", len(book_candidate))

                dict_book_predict = {}
                for book in tqdm(book_candidate):
                    p = self.predict_rate(user, book, enable_print=False)
                    if p is not None:
                        dict_book_predict[book] = p
            else:
                dict_book_predict = {}
                for book in book_candidate:
                    p = self.predict_rate(user, book, enable_print=False)
                    if p is not None:
                        dict_book_predict[book] = p

            sorted_rate_predict = sorted(dict_book_predict.items(), key=lambda x: x[1], reverse=True)
            d_sorted_by_value = collections.OrderedDict(sorted_rate_predict)

            lst = list(d_sorted_by_value.items())
            if len(lst) >= n_pred:
                book_recommendation = lst[0:n_pred]
                # for book, rate in book_recommendation:
                #     print("{book}: {avg}".format(book=book, avg=functions.getMediumRatingBook(book)))
            else:
                high_rate_books = self.functions.high_rate_books[len(lst):n_pred]
                book_recommendation = lst + high_rate_books

        elif enable_print:
            print("User has too few ratings to recommend. ")

        return book_recommendation

    def evaluation(self, test_set, n_samples=20):
        user_rates = {row[0]: [] for row in test_set}
        for row in test_set:
            user = row[0]
            if user not in self.user_book_rating:
                continue
            user_rates[user].append(row[1])

        random.seed(12)
        sub_users = random.sample(user_rates.keys(), k=n_samples)

        f1, ranks, ap = 0, 0, 0
        precision, recall = 0, 0
        for user in tqdm(sub_users):
            # print("User: ", user)
            labels = user_rates[user]
            preds = self.prediction(user, n_pred=10, enable_print=False)
            preds = [book for book, _ in preds]

            pre, rec = precision_recall(labels, preds)
            precision += pre
            recall += rec
            if (pre + rec) != 0:
                f1 += 2 * rec * pre / (rec + pre)

            ranks += rankscore(labels, preds)
            # ap += avg_precision(labels, preds)

        avg_pre = precision / n_samples
        avg_rec = recall / n_samples
        avg_f1 = f1 / n_samples
        avg_ranks = ranks / n_samples
        # ap = ap / n_samples

        return avg_pre, avg_rec, avg_f1, avg_ranks


    def get_error(self, test_set):
        cnt = 0
        cnt_pred = 0
        mae = 0
        mse = 0

        for row in tqdm(test_set):
            if int(row[2]) == 0:
                continue

            cnt += 1
            pred = self.predict_rate(row[0], row[1], enable_print=False)
            if pred is not None:
                cnt_pred += 1
                delta = int(row[2]) - pred
                if delta < 0:
                    delta = -delta
                mae += delta
                mse += delta ** 2

        mae = mae / cnt
        rmse = math.sqrt(mse / cnt)
        return mae, rmse, cnt_pred / cnt
