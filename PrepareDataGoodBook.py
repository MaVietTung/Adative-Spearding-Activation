import csv
import json
import random

user_book = {}
book_user = {}
book_rate = {}
database = 'database2/ratings.csv'
data = csv.reader(open(database))
user_book_with_no_rating_0 = {}
for row in data:
    if(row[0]!='book_id'):
        if user_book.__contains__(row[1]):
            user_book[row[1]][row[0]] = row[2]
        else:
            a = {row[0]: row[2]}
            user_book[row[1]] = a
        if book_user.__contains__(row[0]):
            book_user[row[0]][row[1]] = row[2]
        else:
            a = {row[1]: row[2]}
            book_user[row[0]] = a
        if book_rate.__contains__(row[0]):
            if book_rate[row[0]].__contains__(row[2]):
                book_rate[row[0]][row[2]].append(row[1])
            else:
                book_rate[row[0]][row[2]] = [row[1]]
        else:
            a = {row[2]: [row[1]]}
            book_rate[row[0]] = a
        if row[2] != '0':
            if user_book_with_no_rating_0.__contains__(row[1]):
                user_book_with_no_rating_0[row[1]][row[0]] = row[2]
            else:
                a = {row[0]: row[2]}
                user_book_with_no_rating_0[row[1]] = a
similarities_matrix = {}

for x in user_book.keys():
    a = {}
    similarities_matrix[x] = a
    similarities_matrix[x][x] = 1.0
    for y in user_book[x].keys():
        for z in book_user[y].keys():
            if not similarities_matrix.__contains__(z):
                similarities_matrix[x][z] = random.random()

with open('data_matrix_smilarities_good_book/progess.txt','w') as out_progess:
    out_progess.write('0\n')
    out_progess.write('0\n')

with open('data_matrix_smilarities_good_book/matrix_smilarities.json', 'w') as out_data:
    json.dump(similarities_matrix, out_data)
with open('data_matrix_smilarities_good_book/user_book_rating.json', 'w') as out_data:
    json.dump(user_book, out_data)
with open('data_matrix_smilarities_good_book/book_user_rating.json', 'w') as out_data:
    json.dump(book_user, out_data)
with open('data_matrix_smilarities_good_book/book_rate_user.json', 'w') as out_data:
    json.dump(book_rate, out_data)

with open('data_matrix_smilarities_good_book/user_book_with_no_rating_0.json', 'w') as out_data:
    json.dump(user_book_with_no_rating_0, out_data)
