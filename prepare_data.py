import csv
import json
import random

import pandas as pd
from sklearn.model_selection import train_test_split

from config import *


def split_train_test(data, out_dir, test_size=0.2):
    train_set, test_set = train_test_split(data, test_size=test_size)

    train_path = os.path.join(out_dir, 'train.csv')
    train_set.to_csv(train_path, sep=';', index=False, header=False)

    test_path = os.path.join(out_dir, 'test.csv')
    test_set.to_csv(test_path, sep=';', index=False, header=False)


def prepare_data(data_path):
    user_book = {}
    book_user = {}
    book_rate = {}
    data = csv.reader(open(data_path))
    user_book_with_no_rating_0 = {}

    for row in data:
        string = row[0].split(';')
        if (string[0] != '\ufeffUser-ID') & (len(string) == 3):
            if user_book.__contains__(string[0]):
                user_book[string[0]][string[1]] = string[2]
            else:
                a = {string[1]: string[2]}
                user_book[string[0]] = a
            if book_user.__contains__(string[1]):
                book_user[string[1]][string[0]] = string[2]
            else:
                a = {string[0]: string[2]}
                book_user[string[1]] = a
            if book_rate.__contains__(string[1]):
                if book_rate[string[1]].__contains__(string[2]):
                    book_rate[string[1]][string[2]].append(string[0])
                else:
                    book_rate[string[1]][string[2]] = [string[0]]
            else:
                a = {string[2]: [string[0]]}
                book_rate[string[1]] = a
            if string[2] != '0':
                if user_book_with_no_rating_0.__contains__(string[0]):
                    user_book_with_no_rating_0[string[0]][string[1]] = string[2]
                else:
                    a = {string[1]: string[2]}
                    user_book_with_no_rating_0[string[0]] = a

    similarities_matrix = {}

    for x in user_book.keys():
        a = {}
        similarities_matrix[x] = a
        similarities_matrix[x][x] = 1.0
        for y in user_book[x].keys():
            for z in book_user[y].keys():
                if not similarities_matrix.__contains__(z):
                    similarities_matrix[x][z] = random.random()
    
    similarities_path = os.path.join(os.path.dirname(data_path), 'data_matrix_similarities')
    with open(os.path.join(similarities_path, 'progress.txt'), 'w') as out_progress:
        out_progress.write('0\n')
        out_progress.write('0\n')

    with open(os.path.join(similarities_path, 'matrix_similarities.json'), 'w') as out_data:
        json.dump(similarities_matrix, out_data)
    with open(os.path.join(similarities_path, 'user_book_rating.json'), 'w') as out_data:
        json.dump(user_book, out_data)
    with open(os.path.join(similarities_path, 'book_user_rating.json'), 'w') as out_data:
        json.dump(book_user, out_data)
    with open(os.path.join(similarities_path, 'book_rate_user.json'), 'w') as out_data:
        json.dump(book_rate, out_data)

    with open(os.path.join(similarities_path, 'user_book_with_no_rating_0.json'), 'w') as out_data:
        json.dump(user_book_with_no_rating_0, out_data)


# paths = [BX_path, GB_path]
# for path in paths:
#     ratings = pd.read_csv(os.path.join(path, 'ratings.csv'), sep=';')
#     split_train_test(ratings, path)
#
#     train_path = os.path.join(path, 'train.csv')
#     prepare_data(train_path)
