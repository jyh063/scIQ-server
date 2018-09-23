from flask import Flask
from flask import request
from elasticsearch import Elasticsearch
import json
from models.user import User
from models.post import Post
from models.review import Review
from models.product import Product
from models.tag import Tag
from models.demo import Demo

# initialization
app = Flask(__name__)
es = Elasticsearch()


# define a token to secure update and delete actions
ACCEPT_TOKEN = 'sbPdJBsh8bXf5bJEFNknUfUxs56jVru2XvheMC2xrFNeU2Fepd'



@app.route('/')
def root_call():
    """
    perform when the root route is called
    :return: a default string
    """
    return 'Skinalytics Search API'



@app.route('/product/brand/<brand_name>')
def search_brand(brand_name):
    """
    NOTE: DEPRECATED!!!  Use search_mutiple_brands(route: /product/brands) instead
    :param brand_name: a single brand name read in
    :return: the list of all the products that match the brand name
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    sortby = request.args.get('sortby')
    return Product.search_brands(es, [brand_name], from_, size, sortby)



@app.route('/product/brands', methods=['POST'])
def search_mutiple_brands():
    """
    Read a JSON object containing brands names from the request body and return all the products that
    match any of the brands read in.

    Required Request Body Format:
    {
        "brands": ["brand_name_1", "brand_name_2"]
    }

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results
    sortby: asc or desc, enable the sorting (by rating) option.
            Ignore this parameter to display results in the default order (by matching scores)

    Return the list as json formmat
    :return: the list of all the products that match the brand name
    """
    request.get_data()
    data_obj = json.loads(request.data)

    from_ = request.args.get('from')
    size = request.args.get('size')
    sortby = request.args.get('sortby')

    return Product.search_brands(es, data_obj['brands'], from_, size, sortby)



@app.route('/product/brand/auto_complete/<brand_name>')
def auto_complete_brand(brand_name):
    """
    Read a string from the url and list all the products whose brand name could match such string
    Return the list of product brand names
    :param brand_name: the brand name read in
    :return: the list of all the products that match the string
    """
    return Product.auto_complete_brand_name(es, brand_name)



@app.route('/product/name/<name>')
def show_name(name):
    """
    Read a product name from the url and list all the products that match the name.
    Return the list as json formmat

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results
    sortby: asc or desc, enable the sorting (by rating) option.
            Ignore this parameter to display results in the default order (by matching scores)

    :param name: the product name read in
    :return: the list of all the products that match the name
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    sortby = request.args.get('sortby')
    return Product.search_by_name(es, name, from_, size, sortby)



@app.route('/product/name/auto_complete/<name>')
def auto_complete_product_name(name):
    """
    Read a string from the url and list all the products whose brand name could match such string
    Return the list of product brand names
    :param brand_name: the product name read in
    :return: the list of all the products that match the string
    """
    return Product.auto_complete_product_name(es, name)



@app.route('/product/type/<type_name>')
def search_type(type_name):
    """
    Read a type name from the url and list all the products that match the type.
    Return the list as json formmat

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results
    sortby: asc or desc, enable the sorting (by rating) option.
            Ignore this parameter to display results in the default order (by matching scores)

    :param brand_name: the product type read in
    :return: the list of all the products that match the type
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    sortby = request.args.get('sortby')
    return Product.search_by_type(es, type_name, from_, size, sortby)



@app.route('/product/type/auto_complete/<type_s>')
def auto_complete_type(type_s):
    """
    Read a string from the url and list the types that match the string
    Return the list as json formmat
    :param type_s: the string read in
    :return: the list of all the types that match the string
    """
    return Product.auto_complete_type(es, type_s)



@app.route('/product/ingredients', methods=['POST'])
def search_ingredients():
    """
    NOTE: DEPRECATED!!!  Use search_ingredients_from_request_body(route: /product/ingredients_v2) instead
    :return: the list of products that include certain ingredients and exclude certain ingredients
    """
    ex_str = request.form['exclude']
    in_str = request.form['include']

    ex_list = json.loads(ex_str)
    in_list = json.loads(in_str)

    from_ = request.args.get('from')
    size = request.args.get('size')

    return Product.search_by_ingredients(es, ex_list, in_list, from_, size)



@app.route('/product/ingredients_v2', methods=['POST'])
def search_ingredients_from_request_body():
    """
    Search products by the included ingredients and excluded ingredients

    Required Request Body Format:
    {
        "include": ["ingredient1", "ingredient2"],
        "exclude": ["ingredient3"]
    }

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results
    sortby: asc or desc, enable the sorting (by rating) option.
            Ignore this parameter to display results in the default order (by matching scores)

    :return: the list of products that include certain ingredients and exclude certain ingredients
    """
    request.get_data()
    raw_data = request.data
    data_obj = json.loads(raw_data)

    ex_list = data_obj['exclude']
    in_list = data_obj['include']

    from_ = request.args.get('from')
    size = request.args.get('size')
    sortby = request.args.get('sortby')

    return Product.search_by_ingredients(es, ex_list, in_list, from_, size, sortby)



@app.route('/product/ingredients/auto_complete/<name>')
def auto_complete_ingredients(name):
    """
    Read a string from the url and list the ingredients that match the string
    Return the list as json formmat
    :param name: the string read in
    :return: the list of all the ingredients that match the string
    """
    return Product.auto_complete_ingredients(es, name)



# product search
@app.route('/user/username/<name>')
def search_users(name):
    """
    Read a username from the url and list all the users that match the username
    Return the list as json format

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results

    :param name: the username read in
    :return: the list of all the users that match the username
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    return User.search_users(es, name, from_, size)


@app.route('/user/username/auto_complete/<name>')
def auto_complete_users(name):
    """
    Read a string from the url. If any of the username, first name and last name matches the string, then
    the user info will be returned.
    Return the list as json formmat

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results

    :param name: the string read in
    :return: the list of the users that match the string
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    return User.auto_complete_users(es, name, from_, size)


# review search
@app.route('/review/content/<content>')
def search_reviews(content):
    """
    Read a content from the url and list all the reviews that match the content.
    Return the list as json format
    :param content: the content read in
    :return: the list of all the reviews that match the content
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    return Review.search_reviews(es, content, from_, size)



@app.route('/review/auto_complete/<content>')
def auto_complete_reviews(content):
    """
    Read a string from the url. Return input suggestions based on product info and user info of reviews
    Return the list as json formmat

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results

    :param name: the string read in
    :return: the list of the review suggestions that match the string
    """
    return Review.auto_complete_reviews(es, content)



@app.route('/post/content/<content>')
def search_posts(content):
    """
    Read a string from the url. If any of the username, first name, last name and the post content matches the string,
    the post info will be returned.

    Optional Url Parameters:
    from:   an integer, the beginning index of the search results
    size:   an integer, the max number of the search results

    :param name: the string read in
    :return: the list of the post suggestions that match the string
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    return Post.search_posts(es, content, from_, size)


@app.route('/post/auto_complete/<content>')
def auto_complete_posts(content):
    """
    Read a string from the url. Return input suggestions based on user info of posts
    Return the list as json formmat

    :param name: the string read in
    :return: the list of the post suggestions that match the string
    """
    return Post.auto_complete_posts(es, content)


@app.route('/tag/<tag_name>')
def search_tags(tag_name):
    """
    Read a user id from the url and list all the posts that match the user id.
    Return the list as json format
    :param user_id: the user id read in
    :return: the list of all the posts that match the user id
    """
    from_ = request.args.get('from')
    size = request.args.get('size')
    return Tag.search_tags(es, tag_name, from_, size)



@app.route('/tag/auto_complete/<tag_name>')
def auto_complete_tags(tag_name):
    """
    Read a string from the url and list the tag names that match the string
    :param tag_name: the string read in
    :return: the list of all the types that match the string
    """
    return Tag.auto_complete_tags(es, tag_name)



@app.route('/create/user/', methods=['POST'])
def create_user():
    """
    Crate a new user object in ES
    :return: the created user object in json format
    """
    # check the token
    token = request.form['token']
    if token != ACCEPT_TOKEN:
        return 'Error: not authorized'

    u = User(es)
    return u.create_from_req(request)



@app.route('/create/post/', methods=['POST'])
def create_post():
    """
    Crate a new post object in ES
    :return: the created post object in json format
    """
    # check the token
    token = request.form['token']
    if token != ACCEPT_TOKEN:
        return 'Error: not authorized'

    p = Post(es)
    return p.create_from_req(request)


@app.route('/create/review/', methods=['POST'])
def create_review():
    """
    Create a new review object in ES
    :return: the created review object in json format
    """
    # check the token
    token = request.form['token']
    if token != ACCEPT_TOKEN:
        return 'Error: not authorized'

    r = Review(es)
    return r.create_from_req(request)



# Delete a product
# Not required for now
# @app.route('/delete/product/', methods=['POST'])
# def delete_product():
#     token = request.form['token']
#     if token != ACCEPT_TOKEN:
#         return 'Error: not authorized'
#     pid = request.form['productId_s']
#     es.delete(index='product-index', id=pid, doc_type='data', timeout='2s')
#     return str(pid) + ' deleted'



@app.route('/test_ingredients_api')
def demo_ingredients_api():
    """
    Sample HTML page to demonstrate searching included and excluded ingredients
    :return: the search ingredients demo page
    """
    return Demo.TEST_SEARCH_INGREDIENTS_HTML



@app.route('/auto_complete/demo/')
def auto_complete_demo():
    """
    Sample HTML page to demonstrate the auto-complete function
    :return: the auto-complete demo page
    """
    return Demo.TEST_AUTO_COMPLETE_HTML



@app.route('/test_update_rating/<pid>')
def test_rating(pid):
    """
    Test updating product rating function

    Required Url Parameter:
    rating: an integer, a new rating for a product

    Note: don't use this route in production. The rating will be automatically updated when a review is submitted.
          The method is just for testing.
    :param pid: the product id
    :return: the new rating of the product
    """
    rating = request.args.get('rating')
    if rating == None:
        return "no rating updated"
    return Product.update_rating(es, pid, int(rating))



if __name__ == '__main__':

    local_debug = False         # MUST set False in remote server
    remote_debug = True         # MUST set False in production

    if local_debug:
        app.debug = True
        app.run()
    elif remote_debug:
        app.debug = True
        app.run(host='0.0.0.0', port='80')
    else:
        app.debug = False
        app.run()
