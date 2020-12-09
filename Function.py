def getSmilaritiesValue(user1, user2, maxtrix_similarities):
    if user1 == user2:
        return 1
    if maxtrix_similarities.__contains__(user1):
        if maxtrix_similarities[user1].__contains__(user2):
            return maxtrix_similarities[user1][user2]
    if maxtrix_similarities.__contains__(user2):
        if maxtrix_similarities[user2].__contains__(user1):
            return maxtrix_similarities[user2][user1]
    else:
        return 0


