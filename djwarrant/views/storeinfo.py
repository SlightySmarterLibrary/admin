from django.shortcuts import render
import boto3



# call dynamo from here
def storeinfo(request):
    store_id = request.user.email
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('stores')
    resp = table.query(KeyConditionExpression=Key('id').eq(store_id))


    return render(request, 'warrant/storeinfo.html', {'store_id': store_id, 'resp': resp})

