from django.urls import reverse_lazy
from djwarrant.forms import StoreForm
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.forms import BSModalForm
from dynamodb_json import json_util as json
from django.conf import settings
from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key
from bootstrap_modal_forms.forms import BSModalForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from djwarrant.forms import StoreForm
from django.urls import reverse_lazy
from django.http import HttpResponse



dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('stores')
# call dynamo from here


def storeinfo(request):
    store_id = request.user.email
    store_name = request.user.username
    
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


def update(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        name = form.data['adult']
        print(name)

    return HttpResponse('Form submitted!')

class InventoryView(BSModalCreateView):
    template_name = 'warrant/update-inventory.html'
    form_class = StoreForm

    def get_success_url(self):
        if self.request.method == 'POST':
            form = StoreForm(self.request.POST)
            new_adult = form.data['adult_masks']
            new_children = form.data['children_masks']

            # send to dynamo
            store_id = self.request.user.email
            resp = table.query(KeyConditionExpression=Key('id').eq(store_id))

            try:
                update = table.update_item(
                    Key = { "id": store_id },
                    UpdateExpression="set adult=:a, children=:c",
                    ExpressionAttributeValues={
                    ':a': new_adult,
                    ':c': new_children
                },
                ReturnValues="UPDATED_NEW"
                )
            except Exception as e:
                raise(e)
            
            print("Dynamo updated")

            sqs = boto3.client('sqs', region_name='us-east-1')
            qname = "https://sqs.us-east-1.amazonaws.com/583068504140/homework2"
            arn = resp['Items'][0]['sns_arn']
            name = resp['Items'][0]['name']

            # arn
            x = '''{{"function":"sendEmail", "store": "{0}", "adult": {1}, "children": {2}, "topic": "{3}"}}'''.format(name, new_adult, new_children, arn)
            sqs.send_message(QueueUrl=qname, MessageBody=x)  
            print(x)  
            print("sqs sent!")

        return reverse_lazy('dw:storeinfo')

    def get_initial(self):
      store_id = self.request.user.email
      resp = table.query(KeyConditionExpression=Key('id').eq(store_id))
      adult = resp['Items'][0]['adult']
      children = resp['Items'][0]['children']
      return {
        'adult_masks': adult,
        'children_masks': children
      }

     






