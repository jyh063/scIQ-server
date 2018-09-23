from util import Util
import json

class Product(object):

    @staticmethod
    def search_by_name(es, name, from_, size, sortby):
        """
        Search products through product name
        :param es: the elasticsearch client
        :param name: the name query read in
        :param from_: the beginning index of the results
        :param size: the max size of the results
        :param sortby: the sorting (by rating) option
        :return: the search results in json format
        """
        query_body = {
            "query": {
                "match_phrase": {"name_s": name}
            }
        }

        if sortby != None:
            query_body = {
                "sort": [
                    {"avg_rating_n": sortby}
                ],
                "query": {
                    "match_phrase": {"name_s": name}
                }
            }
        else:
            query_body = {
                "query": {
                    "function_score": {
                        "query": {
                            "match_phrase": {"name_s": name}
                        },
                        "script_score": {
                            "script": {
                                "lang": "groovy",
                                "inline": "Math.log(_score * doc['avg_rating_n'].value * doc['num_ratings_n'].value)",
                            }
                        }
                    }
                }
            }

        es_res = es.search(
            index="product-index",
            body=query_body,
            from_=from_,
            size=size
        )

        # return json.dumps(es_res, indent=4)
        return Util.convert_json_format(es_res)


    @staticmethod
    def search_brands(es, brands_list, from_, size, sortby):
        """
        Search products through brand
        :param es: elasticsearch client
        :param brands_list: the brands from user input
        :param from_: the beginning index of the results
        :param size: the max size of results
        :param sortby: the sorting option for rating
        :return: list of searching results
        """

        query_body = {
            "bool": {
                "should": []
            }
        }

        for brand in brands_list:
            query_body["bool"]["should"].append({"match_phrase": {"brand_s": brand}})

        if sortby != None:
            search_body = {
                "sort": [
                    {"avg_rating_n": sortby}
                ],
                "query": query_body
            }
        else:
            search_body = {
                "query": {
                    "function_score": {
                        "query": query_body,
                        "script_score": {
                            "script": {
                                "lang": "groovy",
                                "inline": "doc['avg_rating_n'].value * doc['num_ratings_n'].value"
                            }
                        }
                    }
                }
            }

        es_res = es.search(
            index="product-index",
            body=search_body,
            from_=from_,
            size=size
        )

        # print json.dumps(es_res, indent=4)

        return Util.convert_json_format(es_res)


    @staticmethod
    def search_by_type(es, type, from_, size, sortby):
        """
        Search products through type
        :param es: elasticsearch client
        :param type: user input
        :param from_: the beginning index of the results
        :param size: the max size of results
        :param sortby: the sorting option for rating
        :return: list of searching results
        """

        query_body = {"query": {"match_phrase": {"type_s": type}}}

        if sortby != None:
            query_body["sort"] = [
                {"avg_rating_n": sortby}
            ]

        es_res = es.search(
            index="product-index",
            body=query_body,
            from_=from_,
            size=size
        )
        return Util.convert_json_format(es_res)


    @staticmethod
    def search_by_ingredients(es, ex_list, in_list, from_, size, sortby):
        """
        Search products through included and excluded ingredients
        :param es: elasticsearch client
        :param ex_list: the list of excluded ingredients
        :param in_list: the list of included ingredients
        :param from_: the beginning index of results
        :param size: the max size of results
        :param sortby: the sorting option for rating
        :return: list of searching results
        """
        must_list = []
        must_not_list = []

        for item in in_list:
            must_list.append({"match_phrase": {"ingredients_ss": item}})

        for item in ex_list:
            must_not_list.append({"match_phrase": {"ingredients_ss": item}})

        query_body = {
            "query": {
                "bool": {
                    "must": must_list,
                    "must_not": must_not_list
                }
            }
        }

        if sortby != None:
            query_body["sort"] = [
                {"avg_rating_n": sortby}
            ]
        else:
            query_body = {
                "query": {
                    "function_score": {
                        "query": query_body["query"],
                        "script_score": {
                            "script": {
                                "lang": "groovy",
                                "inline": "Math.log(_score * doc['avg_rating_n'].value * doc['num_ratings_n'].value)"
                            }
                        }
                    }
                }
            }

        es_res = es.search(index="product-index", body=query_body, from_=from_, size=size)
        return Util.convert_json_format(es_res)


    @staticmethod
    def auto_complete_product_name(es, name):
        """
        Get suggestions for product name based on uesr input
        :param es: elasticsearch client
        :param name: user input
        :return: list of product names that match the uesr input
        """
        query_body = {
            "query": {
                "match_phrase_prefix": {
                    "name_s": name,
                }
            }
        }

        es_res = es.search(index="product-index", body=query_body)

        res = {}
        match_list = []
        for data in es_res['hits']['hits']:
            match_list.append(data['_source']['name_s'])

        res['results'] = Util.sort_results_by_prefix(match_list, name)
        res['num_results'] = len(res['results'])
        return json.dumps(res, indent=4)


    @staticmethod
    def auto_complete_brand_name(es, brand):
        """
        Get suggestions of brand name based on user input
        :param es: elasticsearch client
        :param brand: user input
        :return: list of suggestions that match the user input
        """

        query_body = {
            "query": {
                "match_phrase_prefix": {
                    "brand_s": brand,
                }
            }
        }
        es_res = es.search(index="product-index", body=query_body)
        res = {}

        res['results'] = [data['_source']['brand_s'] for data in es_res['hits']['hits']]
        res['results'] = list(set(res['results']))
        res['results'] = Util.sort_results_by_prefix(res['results'], brand)
        res['num_results'] = len(res['results'])

        return json.dumps(res, indent=4)


    @staticmethod
    def auto_complete_type(es, type_s):
        """
        Get suggestions for type based on
        :param es:
        :param type_s:
        :return:
        """
        query_body = {
            "query": {
                "match_phrase_prefix": {
                    "type_s": type_s,
                }
            }
        }
        es_res = es.search(index="product-index", body=query_body)
        res = {}

        res['results'] = [data['_source']['type_s'] for data in es_res['hits']['hits']]
        res['results'] = list(set(res['results']))
        res['results'] = Util.sort_results_by_prefix(res['results'], type_s)
        res['num_results'] = len(res['results'])

        return json.dumps(res, indent=4)


    @staticmethod
    def auto_complete_ingredients(es, ingredient):
        """
        Get suggestions for ingredients based on user input
        :param es: elasticsearch client
        :param ingredient: user input
        :return: list of ingredient names that match the user input
        """
        query_body = {
            "query": {
                "match_phrase_prefix": {
                    "ingredients_ss": ingredient,
                }
            }
        }
        es_res = es.search(index="product-index", body=query_body)
        res = {}
        match_list = []

        for data in es_res['hits']['hits']:
            ingredients_list = data['_source']['ingredients_ss']
            for i in ingredients_list:
                if i.lower().startswith(ingredient.lower()) or ' ' + ingredient.lower() in i.lower():
                    match_list.append(i)

        res['results'] = list(set(match_list))
        res['results'] = Util.sort_results_by_prefix(res['results'], ingredient)
        res['num_results'] = len(res['results'])
        return json.dumps(res, indent=4)


    @staticmethod
    def update_rating(es, product_id, rating):
        """
        Update rating for a particular product. Increment the num_ratings field and modify the avg_rating field
        accordingly.
        :param es: elasticsearch client
        :param product_id:
        :param rating:
        :return: error if the product id is not found; otherwise return the new avg_rating of the product
        """
        es_res = es.get(index='product-index', doc_type='data', id=product_id)
        if not es_res['found']:
            return "error"

        product = es_res['_source']
        num_ratings = product['num_ratings_n']
        avg_rating = product['avg_rating_n']
        new_rating =  avg_rating * num_ratings + rating
        num_ratings += 1
        new_rating = new_rating * 1.0 / num_ratings

        update_body = {
            "doc": {
                "num_ratings_n": num_ratings,
                "avg_rating_n": new_rating
            }
        }

        es.update(
            index='product-index',
            doc_type='data',
            id=product_id,
            body=update_body
        )

        return product['name_s'] + ": \nNew Rating: " + str(new_rating)

