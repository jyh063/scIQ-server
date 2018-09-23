#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Initialization for the search API
Transform the data from json file to elasticsearch engine
"""

from elasticsearch import Elasticsearch
import json
import csv
import random


def transfer_products_data():
    # read products data from external json file
    jsonFile = open('data/products_dynamo.json')
    dataDict = json.load(jsonFile)
    jsonFile.close()

    # index the products data to elasticsearch
    es = Elasticsearch()

    mapping_config = {

        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        # "type": "standard",
                        "filter": ["lowercase"],
                        "char_filter": [
                            "my_char_filter"
                        ]
                    }
                },
                "char_filter": {
                    "my_char_filter": {
                        "type": "mapping",
                        "mappings": [
                            "\u00e8 => e",
                            "\u2013 => -",
                            "\u00ac => -",
                            "\u00c1 => a",
                            "\u00b7 => .",
                            "\u00a0 => \u0020",
                            "\u00a8 => .",
                            "\u2018 => '",
                            "\u2122 => T",
                            "\u2019 => '",
                            "\u00ba => \u0020",
                            "\u00ae => R",
                            "\u00fc => u",
                            "\u00b0 => \u0020",
                            "\u00c9 => E",
                            "\u00b4 => '"
                        ]
                    }
                }
            }
        },

        "mappings": {
            "data": {
                "properties": {
                    "avg_rating_n": {
                        "type": "double"
                    },
                    "num_ratings_n": {
                        "type": "long"
                    },
                    "brand_s": {
                        "type": "string",
                        "analyzer": "my_analyzer"
                    },
                    "name_s": {
                        "type": "string",
                        "analyzer": "my_analyzer"
                    },
                    "productId_s": {
                        "type": "string",
                        "analyzer": "my_analyzer"
                    },
                    "ingredients_ss": {
                        "type": "string",
                        "analyzer": "my_analyzer"
                    }
                }
            }
        }

    }

    es.indices.create(index='product-index', body=mapping_config)

    for p in dataDict:
        # p['avg_rating_n'] = int(random.uniform(0, 5) * 100) / 100.0
        # p['num_ratings_n'] = int(random.uniform(0, 500))
        p['avg_rating_n'] = 0
        p['num_ratings_n'] = 0
        uuid = p['productId_s']
        es.index(index='product-index', id=uuid, doc_type='data', body=p)
        print "index product: " + p['name_s']


def transfer_posts_data():
    """
    transfer the product data from external json file to elasticsearch
    ES index: product-index
    """
    # read products data from external json file
    jsonFile = open('data/posts.json')
    dataDict = json.load(jsonFile)
    jsonFile.close()

    # index the products data to elasticsearch
    es = Elasticsearch()
    for p in dataDict:
        uuid = p['postId_s']
        es.index(index='post-index', id=uuid, doc_type='data', body=p)



def transfer_reviews_data():
    """
    transfer the product data from external json file to elasticsearch
    ES index: product-index
    """
    # read products data from external json file
    jsonFile = open('data/reviews.json')
    dataDict = json.load(jsonFile)
    jsonFile.close()

    # index the products data to elasticsearch
    es = Elasticsearch()
    for p in dataDict:
        uuid = p['reviewId_s']
        es.index(index='review-index', id=uuid, doc_type='data', body=p)



def load_csv_file(fileName):
    """
    Read data from an external csv file. Return a list of all the items from the csv file. Each list element
    is a dictionary.
    :param fileName: the file to read
    :return: the list of all the data items read in
    """
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)

    data_list = []
    item_keys = []

    for item in reader:
        if reader.line_num == 1:
            # load the first line, read the attribute names
            item_keys = item
            # omit the last four characters (the type) in the attribute name
            for i in range(0, len(item_keys)):
                item_keys[i] = item_keys[i]
            continue

        # load each data item
        dataDict = {}
        for i in range(0, len(item)):
            dataDict[item_keys[i]] = item[i]
        data_list.append(dataDict)

    csvFile.close()
    return data_list



def transfer_user_data():
    """
    transfer users data from csv file to elasticsearch
    ES index: user-index
    """
    data_list = load_csv_file("data/users.csv")
    es = Elasticsearch()
    for item in data_list:
        uuid = item["userId_s"]
        es.index(index='user-index', id=uuid, doc_type='data', body=item)



def transfer_hastag_data():
    """
    transfer hashtags data from csv file to elasticsearch
    ES index: tag-index
    """
    data_list = load_csv_file("data/hashtags.csv")
    es = Elasticsearch()
    for item in data_list:
        uuid = item["timeModified_itemId_s"]
        es.index(index='tag-index', doc_type='data', body=item)



# transfer_reviews_data()
# transfer_posts_data()
# transfer_user_data()
transfer_products_data()

