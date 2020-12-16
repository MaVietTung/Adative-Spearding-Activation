import math
import json
import collections

from tqdm import notebook

from utils.functions import Function
from utils.utils import f1_score, rankscore, avg_precision


class Recommender:
    def __init__(self, user_book_rating, book_rate_user, matrix_similarities, book_user_rate):
        self.user_book_rating = user_book_rating
        self.book_rate_user = book_rate_user
        self.book_user_rate = book_user_rate
        self.matrix_similarities = matrix_similarities
        self.functions = Function(user_book_rating, book_rate_user, matrix_similarities, book_user_rate)

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
                    similarities += self.RMS(item, self.user_book_rating[user_a][item],
                                             self.user_book_rating[user_i][item])
                    len_item += 1
        if len_item != 0:
            return similarities / len_item
        else:
            return 0

    def train(self, epochs=2):
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

        for epoch in range(epochs):
            print('Epoch: ', epoch + 1)
            for active_user in notebook.tqdm(active_list):
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

    def predict_rate(self, user, book):
        predict = None
        if self.user_book_rating.__contains__(user):
            user_rates = self.user_book_rating[user]
            if user_rates.__contains__(book):
                return int(user_rates[book])
            medium_rating_user = self.functions.getMediumRating(user)
            if self.book_rate_user.__contains__(book):
                K = 0
                S = 0
                for rate in self.book_rate_user[book]:
                    if rate != '0':
                        for user_i in self.book_rate_user[book][rate]:
                            w = self.functions.getSimilaritiesValue(user, user_i)
                            S += (int(rate) - self.functions.getMediumRating(user_i)) * w
                            K += w
                            # print('{user}: {rate}, {avg_rate} - {similarity}'.format(user=user_i, rate=rate, avg_rate=self.functions.getMediumRating(user_i), similarity=w))
                if K != 0:
                    predict = medium_rating_user + 1 / K * S
        return predict

    def prediction(self, user, n_pred=20):
        book_recommendation = []

        if self.user_book_rating.__contains__(user):
            medium_rating = self.functions.getMediumRating(user)
            # print("User avg rating: ", medium_rating)

            if medium_rating == 0:
                # print("User does not have any explicit ratings.")
                book_recommendation = self.functions.getHighRateBook()

            else:
                book_candidate = self.functions.getBookCandidate(user)
                # print("Book Candidate: ", len(book_candidate))

                dict_book_predict = {}
                for book in book_candidate:
                    if self.book_rate_user.__contains__(book):
                        p = self.predict_rate(user, book)
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
                    book_recommendation = lst

        # else:
        #     print("User is incorrect. Please Enter another user ID. ")

        return book_recommendation

    def get_mae(self, test_set):
        cnt = 0
        mae = 0
        mse = 0
        for row in test_set:
            pred = self.predict_rate(row[0], row[1])
            if pred is not None:
                cnt += 1
                delta = int(row[2]) - pred
                if delta < 0:
                    delta = -delta
                mae += delta
                mse += delta ** 2

        mae = mae / cnt
        rmse = math.sqrt(mse / cnt)
        return mae, rmse, cnt / len(test_set)

    def get_score(self, test_set, mode='rankscore'):
        ground_truth = {row[0]: [] for row in test_set}
        for row in test_set:
            user = row[0]
            ground_truth[user].append([row[1], int(row[2])])

        f1, ranks, ap = 0, 0, 0
        for user in ground_truth:
            # ground_truth[user].sort(key=lambda x: x[1])
            labels = [book for book, _ in ground_truth[user]]

            preds = self.prediction(user, n_pred=10)
            preds = [book for book, _ in preds]

            if mode == 'f1_score':
                f1 += f1_score(labels, preds)
            elif mode == 'rankscore':
                ranks += rankscore(labels, preds)
            elif mode == 'avg_precision':
                ap += avg_precision(labels, preds)
            else:
                f1 += f1_score(labels, preds)
                ranks += rankscore(labels, preds)
                ap += avg_precision(labels, preds)

        f1 = f1 / len(ground_truth)
        ranks = ranks / len(ground_truth)
        ap = ap / len(ground_truth)

        return f1, ranks, ap
