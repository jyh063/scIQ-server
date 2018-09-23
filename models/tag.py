import json
from util import Util


class Tag(object):

    @staticmethod
    def search_tags(es, tag_name, from_, size):
        """
        Search posts and reviews based on tag names
        :param es: elasticsearch client
        :param tag_name: user input
        :param from_: the beginning index of results
        :param size: the max size(for review or post) of results
        :return: list of search results
        """
        es_post_res = es.search(
            index="post-index",
            body={"query": {"match": {"tags_ss": tag_name}}},
            from_=from_,
            size=size
        )
        es_review_res = es.search(
            index="review-index",
            body={"query": {"match": {"tags_ss": tag_name}}},
            from_=from_,
            size=size
        )

        res = {}
        res['num_results'] = len(es_post_res['hits']['hits']) + len(es_review_res['hits']['hits'])
        match_list = []

        for data in es_post_res['hits']['hits']:
            post_item = data['_source']
            post_item['content_type'] = 'post'
            match_list.append(post_item)

        for data in es_review_res['hits']['hits']:
            review_item = data['_source']
            review_item['content_type'] = 'review'
            match_list.append(review_item)

        res['results'] = match_list

        return json.dumps(res, indent=4)



    @staticmethod
    def auto_complete_tags(es, tag):
        """
        Get input suggestions for tag search
        :param es: elasticsearch client
        :param tag: user input
        :return: list of suggestted tag names
        """
        query_body = {
            "query": {
                "match_phrase_prefix": {
                    "tags_ss": tag,
                }
            }
        }

        res = {}
        match_list = []

        es_res = es.search(index="post-index", body=query_body)

        for data in es_res['hits']['hits']:
            tags_list = data['_source']['tags_ss']
            for t in tags_list:
                if t.lower().startswith(tag.lower()):
                    match_list.append(t)

        es_res = es.search(index="review-index", body=query_body)

        for data in es_res['hits']['hits']:
            tags_list = data['_source']['tags_ss']
            for t in tags_list:
                if t.lower().startswith(tag.lower()):
                    match_list.append(t)

        res['results'] = list(set(match_list))
        res['num_results'] = len(res['results'])
        return json.dumps(res, indent=4)
