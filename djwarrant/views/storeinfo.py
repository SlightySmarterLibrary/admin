from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key
from django.conf import settings
from dynamodb_json import json_util as json

# call dynamo from here


def storeinfo(request):
    store_id = request.user.email
    store_name = request.user.username
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('stores')
    resp = table.query(KeyConditionExpression=Key('id').eq(store_id))
    adult = resp['Items'][0]['adult']
    children = resp['Items'][0]['children']

    orders = ViewOrders().process(store_id=store_id, received=False)

    return render(request, 'warrant/storeinfo.html', {'store_name': store_name, 'adult': adult, 'children': children, 'orders': orders})


class ViewOrders():
    """Loads Orders from DynamoDB"""

    def process(self, store_id=None, received=False):
        dynamoDB = boto3.client('dynamodb', region_name=settings.AWS_REGION)

        response = dynamoDB.query(
            TableName='orders',
            IndexName='store_id-index',
            KeyConditionExpression="store_id = :store_id",
            ExpressionAttributeValues={
                ':store_id': {'S': store_id},
            })

        return json.loads(response['Items'])
