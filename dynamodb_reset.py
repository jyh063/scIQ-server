## This file is not part of the project in server
## This is a script to reset the avg_rating and num_reviews fields to 0 for all the products in DynamoDB

import boto3
import decimal

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAJEHZUUC5WV42COUQ',
    aws_secret_access_key='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',
    region_name='us-west-1'
)

product = dynamodb.Table('sciqandroid-mobilehub-631333021-Products')

res, jsonList = product.scan(), []


x = 0

for item in res['Items']:
    response = product.update_item(
        Key={
            'name': item['name'],
            'brand': item['brand']
        },
        UpdateExpression='SET #num_reviews = :val',
        ExpressionAttributeNames={'#num_reviews': "num_reviews"},
        ExpressionAttributeValues={':val': decimal.Decimal(0)},
    )
    x += 1
    print str(x) + ' ' + item['name']


for item in res['Items']:
    response = product.update_item(
        Key={
            'name': item['name'],
            'brand': item['brand']
        },
        UpdateExpression='SET #avg_rating = :val',
        ExpressionAttributeNames={'#avg_rating': "avg_rating"},
        ExpressionAttributeValues={':val': decimal.Decimal(0)},
    )
    x += 1
    print str(x) + ' ' + item['name']


