import json
from util import Util
from datetime import datetime

class Post(object):

    def __init__(self, es):
        """
        constructor: create a post dictionary object and initialize Elasticsearch client instance
        :param es: elasticsearch client
        """
        self.postDict ={
        }
        self.es = es


    def create_from_req(self, request):
        """
        create a new post object and store it in ES
        :param request: the request from flask
        :return: the newly created post in json format
        """
        self.postDict['commentCount_n'] = request.form['commentCount_n']
        self.postDict['likeCount_n'] = request.form['likeCount_n']
        self.postDict['postId_s'] = request.form['postId_s']
        self.postDict['timeModified_s'] = request.form['timeModified_s']
        self.postDict['isPrivate_n'] = request.form['isPrivate_n']
        self.postDict['username_s'] = request.form['username_s']
        self.postDict['lastName_s'] = request.form['lastName_s']
        self.postDict['firstName_s'] = request.form['firstName_s']
        self.postDict['imgUrls_l'] = request.form['imgUrls_l']
        self.postDict['content_s'] = request.form['content_s']
        self.postDict['timeCreated_s'] = request.form['timeCreated_s']
        self.postDict['userId_s'] = request.form['userId_s']
        self.postDict['fullName_s'] = request.form['fullName_s']
        self.postDict['profilePicUrl_s'] = request.form['profilePicUrl_s']
        tags_str = request.form['tags_ss']
        self.postDict['tags_ss'] = json.loads(tags_str)

        self.es.index(index='post-index', id=self.postDict['postId_s'], doc_type='data', body=self.postDict)
        return json.dumps(self.postDict, indent=4)


    @staticmethod
    def search_posts(es, content, from_, size):
        """
        Search posts based on post content and user info
        :param es: elasticsearch client
        :param content: uesr input
        :param from_: the beginning index of the results
        :param size: the max size of the results
        :return: list of search results
        """

        today = datetime.today()
        y = today.year
        m = today.month
        if m < 10:
            cur_month_str = str(y) + '-0' + str(m)
        else:
            cur_month_str = str(y) + '-' + str(m)
        m -= 1
        if m < 1:
            m = 12
            y -= 1
        if m < 10:
            prev_month_str = str(y) + '-0' + str(m)
        else:
            prev_month_str = str(y) + '-' + str(m)


        query_body = {
            "query": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "query": content,
                            "type": "cross_fields",
                            "operator": "or",
                            "fields": [
                                "username_s",
                                "lastName_s",
                                "content_s",
                                "firstName_s",
                                "fullName_s"
                            ]
                        }
                    },
                    "boost": "5",
                    "functions": [
                      {
                          "filter": {
                              "range" : {
                                  "timeModified_s" : {
                                      "gte" : "now-10d/d"
                                  }
                              }
                          },
                          "weight": 40
                      },
                      {
                          "filter": {
                              "range" : {
                                  "timeModified_s" : {
                                      "gte" : "now-30d/d"
                                  }
                              }
                          },
                          "weight": 30
                      },
                      {
                          "filter": {
                              "range" : {
                                  "timeModified_s" : {
                                      "gte" : "now-60d/d"
                                  }
                              }
                          },
                          "weight": 20
                      },
                      {
                          "filter": {
                              "range" : {
                                  "timeModified_s" : {
                                      "gte" : "now-90d/d"
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
        es_res = es.search(index="post-index", body=query_body, from_=from_, size=size)
        return Util.convert_json_format(es_res)


    @staticmethod
    def auto_complete_posts(es, name):
        """
        Get input suggestions for post search based on user info
        :param es: elasticsearch client
        :param name: user input
        :return: list of suggestions
        """
        query_body = {
            "query": {
                "multi_match": {
                    "fields": ["username_s", "lastName_s", "firstName_s"],
                    "query": name,
                    "type": "phrase_prefix"
                }
            }
        }

        es_res = es.search(index="post-index", body=query_body)

        res = {}
        match_list = []
        for data in es_res['hits']['hits']:
            p = data['_source']
            if p['username_s'].lower().startswith(name.lower()):
                match_list.append(p['username_s'])
            elif p['lastName_s'].lower().startswith(name.lower()):
                match_list.append(p['lastName_s'])
            elif p['firstName_s'].lower().startswith(name.lower()):
                match_list.append(p['firstName_s'])


        res['results'] = list(set(match_list))
        res['num_results'] = len(res['results'])
        return json.dumps(res, indent=4)
