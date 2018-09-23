import json
from util import Util

class User(object):

    def __init__(self, es):
        """
        constructor: create a user dictionary object and initialize Elasticsearch client instance
        :param es: elasticsearch client
        """
        self.userDict ={
        }
        self.es = es

    def create_from_req(self,request):
        """
        index a new user document in ES
        :param request: flask request object
        :return: the newly created user object in json format
        """

        self.userDict['userId'] = request.form['userId_s']
        self.userDict['birthday'] = request.form['birthday_s']
        self.userDict['location'] = request.form['location_s']
        self.userDict['profilePicUrl'] = request.form['profilePicUrl_s']
        self.userDict['shortDescription'] = request.form['shortDescription_s']
        self.userDict['username'] = request.form['username_s']
        self.userDict['postsPrivate'] = request.form['postsPrivate_n']
        self.userDict['photoId'] = request.form['photoId_s']
        self.userDict['gender'] = request.form['gender_s']
        self.userDict['ethnicity'] = request.form['ethnicity_s']
        self.userDict['race'] = request.form['race_s']
        self.userDict['email'] = request.form['email_s']
        self.userDict['original_username'] = request.form['original_username_s']
        self.userDict['firstName'] = request.form['firstName_s']
        self.userDict['lastName'] = request.form['lastName_s']
        self.userDict['fullName'] = request.form['fullName_s']
        self.userDict['facebookId'] = request.form['facebookId_s']

        self.es.index(index='user-index', id=self.userDict['userId'], doc_type='data', body=self.userDict)
        return json.dumps(self.userDict, indent=4)


    @staticmethod
    def search_users(es, name, from_, size):
        """
        Search users through username, last name or first name
        :param es: elasticsearch client
        :param name: user input
        :param from_: the beginning index of results
        :param size: the max size of results
        :return: list of searching results
        """
        query_body = {
            "query": {
                "multi_match": {
                    "query": name,
                    "type": "cross_fields",
                    "operator": "or",
                    "fields": [
                        "username",
                        "lastName"
                        "firstName",
                        "fullName"
                    ]
                }
            }
        }
        es_res = es.search(index="user-index", body=query_body, from_=from_, size=size)
        print str(es_res)
        return Util.convert_json_format(es_res)


    @staticmethod
    def auto_complete_users(es, name, from_, size):
        """
        Get suggestions for uesrs search based on username, first name and last name
        :param es: elasticsearch client
        :param name: user input
        :param from_: the beginning index of results
        :param size: the max size of results
        :return: list of suggestions
        """
        query_body = {
            "query" : {
                "multi_match" : {
                    "fields" : ["username", "lastName", "firstName", "fullName"],
                    "query": name,
                    "type" : "phrase_prefix"
                }
            }
        }
        es_res = es.search(index="user-index", body=query_body, from_=from_, size=size)
        return Util.convert_json_format(es_res)