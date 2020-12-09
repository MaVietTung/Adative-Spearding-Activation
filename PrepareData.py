import csv
import json
import random

user_book = {}
book_user = {}
book_rate = {}
database = 'database/BX-Book-Ratings.csv'
data = csv.reader(open(database))

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
similarities_matrix = {}
for x in user_book.keys():
    a = {}
    similarities_matrix[x] = a
    similarities_matrix[x][x] = 1.0
    for y in user_book[x].keys():
        for z in book_user[y].keys():
            if not similarities_matrix.__contains__(z):
                similarities_matrix[x][z] = random.random()
with open('data_matrix_smilarities/progess.txt') as out_progess:
    out_progess.write('0\n')
    out_progess.write('0\n')
with open('data_matrix_smilarities/matrix_smilarities.json', 'w') as out_data:
    json.dump(similarities_matrix, out_data)
with open('data_matrix_smilarities/user_book_rating.json', 'w') as out_data:
    json.dump(user_book, out_data)
with open('data_matrix_smilarities/book_user_rating.json', 'w') as out_data:
    json.dump(book_user, out_data)
with open('data_matrix_smilarities/book_rate_user.json', 'w') as out_data:
    json.dump(book_rate, out_data)
