import collections
import math


class Function:
    def __init__(self, user_book_rating, book_rate_user, matrix_similarities, book_user_rate, dataset=1):
        self.user_book_rating = user_book_rating
        self.book_rate_user = book_rate_user
        self.book_user_rate = book_user_rate
        self.matrix_similarities = matrix_similarities
        self.high_rate_books = self.getHighRateBook(dataset)

    def getSimilaritiesValue(self, user1, user2):
        if user1 == user2:
            return 1
        if self.matrix_similarities.__contains__(user1):
            if self.matrix_similarities[user1].__contains__(user2):
                return float(self.matrix_similarities[user1][user2])
        if self.matrix_similarities.__contains__(user2):
            if self.matrix_similarities[user2].__contains__(user1):
                return float(self.matrix_similarities[user2][user1])
        return 0

    def getMediumRating(self, user):
        total = 0
        total_rating = 0
        book_rating = self.user_book_rating[user]
        for book in book_rating.keys():
            if book_rating[book] != '0':
                total += 1
                total_rating += int(book_rating[book])
        if total != 0:
            return total_rating / total
        else:
            return 0

    def getBookCandidate(self, user):
        book_candidate = []
        user_similarities = []
        for book in self.user_book_rating[user].keys():
            if self.book_rate_user.__contains__(book):
                for rate in self.book_rate_user[book].keys():
                    # if rate != '0':
                    user_similarities = user_similarities + self.book_rate_user[book][rate]

        if user_similarities.__contains__(user):
            user_similarities.remove(user)

        for user_i in user_similarities:
            if self.user_book_rating.__contains__(user_i):
                book_candidate = book_candidate + list(self.user_book_rating[user_i].keys())

        book_candidate = list(dict.fromkeys(book_candidate))

        for book in self.user_book_rating[user].keys():
            if book_candidate.__contains__(book):
                book_candidate.remove(book)

        return book_candidate

    def getHighRateBook(self, dataset=1):
        dictionary = {}
        for book in self.book_user_rate:
            # for rate in self.book_rate_user[book]:
            #     if rate != '0':
            #         rating += int(rate) * len(list(self.book_rate_user[book][rate]))
            #         total += len(list(self.book_rate_user[book][rate]))
            #         dictionary[book] = rating / total

            rating = 0
            total = 0
            num = 0
            for user in self.book_user_rate[book]:
                rate = int(self.book_user_rate[book][user])
                if rate != 0:
                    total += 1
                    rating += rate
                num += 1

            if total == 0:
                total += 1
            if num == 0:
                num += 1
            dictionary[book] = ((math.log(num) / dataset) + (rating / total)) / 2
        d_sorted_by_value = collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
        lst = list(d_sorted_by_value.items())
        if len(lst) >= 20:
            return lst[0:20]
        else:
            return lst

    def getMediumRatingBook(self, book):
        rating = 0
        rate_total = 0

        rate_user = self.book_rate_user[book]
        for rate in rate_user:
            if rate != '0':
                cnt = len(rate_user[rate])
                rating += int(rate) * cnt
                rate_total += cnt
        if rate_total != 0:
            return rating / rate_total
        else:
            return 0
