"""
convert data into json
"""

import uuid
import json
import init
import random

def convert_product():
    # read products data from external json file
    jsonFile = open('data/products.json')
    dataDict = json.load(jsonFile, encoding='utf-8')
    jsonFile.close()
    outFile = open('products.json', 'w')
    outFile.write(json.dumps(dataDict, indent=4, ensure_ascii=False))
    outFile.close()


def convert_user():
    data_list = init.load_csv_file("data/users.csv")
    f = open('users.json', 'w')
    f.write(json.dumps(data_list, indent=4))
    f.close()


def convert_post():
    data_list = init.load_csv_file("data/posts.csv")
    user_list = init.load_csv_file("data/users.csv")
    f = open('posts.json', 'w')
    for i in range(0, len(data_list)):
        uid = data_list[i]['userId_s']
        user = search_user(uid, user_list)
        if user == None:
            print i
            data_list[i]['lastName_s'] = ""
            data_list[i]['firstName_s'] = ""
            data_list[i]['fullName_s'] = ""
            data_list[i]['username_s'] = ""
            tag = 'tag' + str(i / 10)
            data_list[i]['tags_ss'] = [tag]
            continue
        data_list[i]['lastName_s'] = user['lastName_s']
        data_list[i]['firstName_s'] = user['firstName_s']
        data_list[i]['fullName_s'] = user['fullName_s']
        data_list[i]['username_s'] = user['username_s']
        tag = 'tag' + str(i / 10)
        data_list[i]['tags_ss'] = [tag]
    f.write(json.dumps(data_list, indent=4))
    f.close()


def convert_reviews():
    data_list = init.load_csv_file("data/reviews.csv")
    user_list = init.load_csv_file("data/users.csv")
    f = open('reviews.json', 'w')
    for i in range(0, len(data_list)):
        uid = data_list[i]['userId_s']
        user = search_user(uid, user_list)
        if user == None:
            print i
            data_list[i]['lastName_s'] = ""
            data_list[i]['firstName_s'] = ""
            data_list[i]['fullName_s'] = ""
            data_list[i]['username_s'] = ""
            tag = 'tag' + str(i / 10)
            data_list[i]['tags_ss'] = [tag]
            continue
        data_list[i]['lastName_s'] = user['lastName_s']
        data_list[i]['firstName_s'] = user['firstName_s']
        data_list[i]['fullName_s'] = user['fullName_s']
        data_list[i]['username_s'] = user['username_s']
        tag = 'tag' + str(i / 10)
        data_list[i]['tags_ss'] = [tag]
    f.write(json.dumps(data_list, indent=4))
    f.close()


def search_user(user_id, user_list):
    for u in user_list:
        if u['userId_s'] == user_id:
            return u
    return None


def get_random_user(user_list):
    index = random.randint(1, len(user_list))
    return user_list[index]


convert_reviews()