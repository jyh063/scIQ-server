
import json
from difflib import SequenceMatcher

class Util(object):

    @staticmethod
    def convert_json_format(es_res):
        """
        read and reformat the data returned by ES
        :param es_res: the json format data returned by elasticsearch
        :return: the json format data for the API calls
        """
        res = {}
        res['num_results'] = len(es_res['hits']['hits'])
        match_list = []
        for data in es_res['hits']['hits']:
            match_list.append(data['_source'])
        res['results'] = match_list
        return json.dumps(res, indent=4)


    @staticmethod
    def sort_results_by_prefix(res_list, query):
        """
        Sort results based on user input.
        :param res_list: the results list
        :param query: user input
        :return:
        """
        match_prefix_list = []          # the list input
        match_others_list = []          #
        for res in res_list:
            if res.lower().startswith(query.lower()):
                match_prefix_list.append(res)
            else:
                match_others_list.append(res)

        match_prefix_list = Util.case_insensitive_sort(match_prefix_list)
        match_others_list = Util.case_insensitive_sort(match_others_list)
        return match_prefix_list + match_others_list


    @staticmethod
    def case_insensitive_sort(liststring):
        """
        sort a list of strings
        :param liststring: the original list
        :return: the sorted list
        """
        listtemp = [(x.lower(), x) for x in liststring]
        listtemp.sort()
        return [x[1] for x in listtemp]


    @staticmethod
    def contains_key(content, key):
        """
        check whether a string contains a particular key word
        :param content: the string to be checked
        :param key: the key word
        :return: whether the string contains the key
        """
        return content.lower().startswith(key.lower()) or ' ' + key.lower() in content.lower()
