import json
import Function as function

with open('data_matrix_smilarities/user_book_rating.json') as fin:
    user_book_rating = json.load(fin)
with open('data_matrix_smilarities/book_user_rating.json') as fin:
    book_user_rating = json.load(fin)
with open('data_matrix_smilarities/matrix_smilarities.json') as fin:
    matrix_smilarities = json.load(fin)
with open('data_matrix_smilarities/book_rate_user.json') as fin:
    book_rate_user = json.load(fin)


def RMS(item_i, rating_x, rating_y):
    R_x_i = book_rate_user[item_i][rating_x]
    R_y_i = book_rate_user[item_i][rating_y]
    result = 0
    w = 1 / len(R_x_i) * 1 / len(R_y_i)
    total = 0
    for user_s in R_x_i:
        for user_t in R_y_i:
            total += function.getSmilaritiesValue(user_s, user_t, matrix_smilarities)
    result = total * w
    return result


def caculate(user_a, user_i):
    smilarities = 0
    len_item = 0
    for item in user_book_rating[user_a].keys():
        if user_book_rating[user_i].__contains__(item):
            if user_book_rating[user_a][item] != user_book_rating[user_i][item]:
                smilarities += RMS(item, user_book_rating[user_a][item], user_book_rating[user_i][item])
                len_item += 1
    if len_item != 0:
        return smilarities / len_item
    else:
        return 0


with open('data_matrix_smilarities/progess.txt', 'r') as fin:
    progess = fin.readline()
    epochs = fin.readline()
progess = int(progess)
epochs = int(epochs)
print('continue train for progess and epoch:', progess, epochs)
if (progess != 0) | (epochs != 0):
    with open('data_matrix_smilarities/result_train_smilarites.json') as fin:
        matrix_smilarities = json.load(fin)
total_progess=len(matrix_smilarities.keys())
active_list = list(matrix_smilarities.keys())
for epoch in range(4 - epochs):
    rint('epoch: ', epoch)
    for active_user in active_list[progess:-1]:
        progess += 1
        print(progess, '/' ,total_progess)
        if progess % 1000 == 0:
            with open('data_matrix_smilarities/result_train_smilarites.json', 'w') as fout:
                json.dump(matrix_smilarities, fout)
            with open('data_matrix_smilarities/progess.txt', 'w') as fout:
                fout.write(str(progess) + '\n')
                fout.write(str(epoch) + '\n')
            print('saved\n')
        for user_i in matrix_smilarities[active_user].keys():
            if active_user != user_i:
                t = caculate(active_user, user_i)
                if t != 0:
                    matrix_smilarities[active_user][user_i] = t

with open('data_matrix_smilarities/result_train_smilarites.json', 'w') as fout:
    json.dump(matrix_smilarities, fout)
