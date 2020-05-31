from django.urls import reverse_lazy
from djwarrant.forms import StoreForm
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.forms import BSModalForm
from dynamodb_json import json_util as json
from django.conf import settings
from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key
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


class InventoryView(BSModalCreateView):
    template_name = 'warrant/update-inventory.html'
    form_class = StoreForm
    success_message = 'Success: Store updated.'
    success_url = reverse_lazy('index')
