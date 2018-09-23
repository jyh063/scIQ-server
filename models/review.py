import json
from util import Util
from product import Product

class Review(object):


    def __init__(self, es):
        """
        constructor: create a post dictionary object and initialize Elasticsearch client instance
        :param es: elasticsearch client
        """
        self.reviewDict = {
        }
        self.es = es


    def create_from_req(self, request):
        """
        index a new review document in ES
        update the product rating with the new rating uploaded
        :param request: flask request object
        :return: the newly created user object in json format
        """

        self.reviewDict['commentCount_n'] = request.form['commentCount_n']
        self.reviewDict['likeCount_n'] = request.form['likeCount_n']
        self.reviewDict['reacted_n'] = request.form['reacted_n']
        self.reviewDict['timeModified_s'] = request.form['timeModified_s']
        self.reviewDict['productName_s'] = request.form['productName_s']
        self.reviewDict['username_s'] = request.form['username_s']
        self.reviewDict['profilePicUrl_s'] = request.form['profilePicUrl_s']
        self.reviewDict['firstName_s'] = request.form['firstName_s']
        self.reviewDict['productId_s'] = request.form['productId_s']
        self.reviewDict['rating_n'] = request.form['rating_n']
        self.reviewDict['content_s'] = request.form['content_s']
        self.reviewDict['timeCreated_s'] = request.form['timeCreated_s']
        self.reviewDict['lastName_s'] = request.form['lastName_s']
        self.reviewDict['productBrand_s'] = request.form['productBrand_s']
        self.reviewDict['reviewId_s'] = request.form['reviewId_s']
        self.reviewDict['fullName_s'] = request.form['fullName_s']
        self.reviewDict['userId_s'] = request.form['userId_s']
        self.reviewDict['coverPhotoUrl_s'] = request.form['coverPhotoUrl_s']

        # load list values
        img_urls_str = request.form['imgUrls_ss']
        self.reviewDict['imgUrls_ss'] = json.loads(img_urls_str)
        tags_str = request.form['tags_ss']
        self.reviewDict['tags_ss'] = json.loads(tags_str)

        # index the review
        self.es.index(index='review-index', id=self.reviewDict['reviewId_s'], doc_type='data', body=self.reviewDict)

        # update product rating
        retVal = Product.update_rating(self.es, self.reviewDict['productId_s'], float(self.reviewDict['rating_n']))

        if retVal == "error":
            return "fail to update rating"
        return json.dumps(self.reviewDict, indent=4)


    @staticmethod
    def search_reviews(es, content, from_, size):
        """
        Serach reviews through product brand, product name, review content and user info
        :param es: elasticsearch client
        :param content: the user input for searching
        :param from_: the beginning index of the results
        :param size: the max size of the results
        :return: list of reviews that match the user input
        """
        query_body = {
            "query": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "query": content,
                            "type": "cross_fields",
                            "operator": "or",
                            "fields": [
                                "productBrand_s",
                                "productName_s",
                                "content_s",
                                "username_s",
                                "lastName_s",
                                "firstName_s",
                                "fullName_s",
                                "tags_ss"
                            ]
                        }
                    },
                    "boost": "5",
                    "functions": [
                        {
                            "filter": {
                                "range": {
                                    "timeModified_s": {
                                        "gte": "now-10d/d"
                                    }
                                }
                            },
                            "weight": 40
                        },
                        {
                            "filter": {
                                "range": {
                                    "timeModified_s": {
                                        "gte": "now-30d/d"
                                    }
                                }
                            },
                            "weight": 30
                        },
                        {
                            "filter": {
                                "range": {
                                    "timeModified_s": {
                                        "gte": "now-60d/d"
                                    }
                                }
                            },
                            "weight": 20
                        },
                        {
                            "filter": {
                                "range": {
                                    "timeModified_s": {
                                        "gte": "now-90d/d"
                                    }
                                }
                            },
                            "weight": 10
                        }
                    ],
                    "max_boost": 40,
                    "score_mode": "max",
                    "boost_mode": "multiply"
                }
            }
        }

        es_res = es.search(index="review-index", body=query_body, from_=from_, size=size)
        return Util.convert_json_format(es_res)


    @staticmethod
    def auto_complete_reviews(es, query):
        """
        Get a list of suggestions from the uesr input based on product info and user info
        :param es: elasticsearch client
        :param query: the user input
        :return: a list of keywords whose prefixes match the user input
        """
        query_body = {
            "query": {
                "multi_match": {
                    "fields": ["productBrand_s", "productName_s", "firstName_s", "lastName_s"],
                    "query": query,
                    "type": "phrase_prefix"
                }
            }
        }

        es_res = es.search(index="review-index", body=query_body)

        res = {}
        match_list = []
        for data in es_res['hits']['hits']:
            review = data['_source']
            if Util.contains_key(review['productBrand_s'], query):
                match_list.append(review['productBrand_s'])
            if Util.contains_key(review['productName_s'], query):
                match_list.append(review['productName_s'])
            if Util.contains_key(review['firstName_s'], query):
                match_list.append(review['firstName_s'])
            elif Util.contains_key(review['lastName_s'], query):
                match_list.append(review['lastName_s'])

        res['results'] = list(set(match_list))
        res['num_results'] = len(res['results'])
        return json.dumps(res, indent=4)
