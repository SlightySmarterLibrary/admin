from django.urls import reverse_lazy
from djwarrant.forms import StoreForm
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.forms import BSModalForm
from dynamodb_json import json_util as json
import json as og_json
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

    order_status = request.GET.get('status', 'all')
    orders = ViewOrders().process(store_id=store_id, status=order_status)

    return render(request,
                  'warrant/storeinfo.html',
                  {
                      'store_name': store_name,
                      'adult': adult,
                      'children': children,
                      'orders': orders,
                      'filter_status': order_status.capitalize()
                  })


class ViewOrders():
    """Loads Orders from DynamoDB"""

    def process(self, store_id=None, status='all'):
        index = 'store_id-index'
        queryCondition = 'store_id = :store_id'
        queryAttributes = {
            ':store_id': store_id
        }

        dynamoDB = boto3.client('dynamodb', region_name=settings.AWS_REGION)
        response = dynamoDB.query(
            TableName='orders',
            IndexName=index,
            KeyConditionExpression=queryCondition,
            ExpressionAttributeValues=og_json.loads(json.dumps(queryAttributes)))

        return filter_results(data=json.loads(response['Items']), status=status)


def filter_results(data, status='all'):
    if status == 'all':
        return data
    elif status == 'pending':
        return list(filter(lambda x: x['received'] == False, data))
    elif status == 'completed':
        return list(filter(lambda x: x['received'] == True, data))


class InventoryView(BSModalCreateView):
    template_name = 'warrant/update-inventory.html'
    form_class = StoreForm
    success_message = 'Success: Store updated.'
    success_url = reverse_lazy('index')
