from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key
from bootstrap_modal_forms.forms import BSModalForm
from bootstrap_modal_forms.generic import BSModalCreateView
from djwarrant.forms import StoreForm
from django.urls import reverse_lazy







# call dynamo from here
def storeinfo(request):
    store_id = request.user.email
    store_name = request.user.username
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('stores')
    resp = table.query(KeyConditionExpression=Key('id').eq(store_id))
    adult = resp['Items'][0]['adult']
    children = resp['Items'][0]['children']


    return render(request, 'warrant/storeinfo.html', {'store_name': store_name, 'adult': adult, 'children': children})


class InventoryView(BSModalCreateView):
    template_name = 'warrant/update-inventory.html'
    form_class = StoreForm
    success_message = 'Success: Store updated.'
    success_url = reverse_lazy('index')



