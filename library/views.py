from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import boto3


def index(request):
    return HttpResponse('Home page')


def browse(request):
    # Get access token
    client = boto3.client('cognito-identity',
                          region_name=settings.AWS_REGION)
    # Get credentials for authenticated user
    try:
        resp = client.get_id(IdentityPoolId=settings.COGNITO_IDENTITY_POOL,
                             Logins={
                                 'cognito-idp.'+settings.AWS_REGION+'.amazonaws.com/'+settings.COGNITO_USER_POOL_ID: request.session['ID_TOKEN']
                             })
        resp = client.get_credentials_for_identity(IdentityId=resp['IdentityId'],
                                                   Logins={
                                                       'cognito-idp.'+settings.AWS_REGION+'.amazonaws.com/'+settings.COGNITO_USER_POOL_ID: request.session['ID_TOKEN']
        })
    # Otherwise, get credential for unauthenticated user
    except:
        resp = client.get_id(IdentityPoolId=settings.COGNITO_IDENTITY_POOL)
        resp = client.get_credentials_for_identity(
            IdentityId=resp['IdentityId'])

    secretKey = resp['Credentials']['SecretKey']
    accessKey = resp['Credentials']['AccessKeyId']
    sessionToken = resp['Credentials']['SessionToken']

    client = boto3.client('dynamodb', aws_access_key_id=accessKey,
                          aws_secret_access_key=secretKey, aws_session_token=sessionToken,
                          region_name=settings.AWS_REGION)
    response = client.scan(TableName=settings.DYNAMODB_BOOKS)
    booklist = sorted(response['Items'], key=lambda k: int(k['id']['S']))
    paginator = Paginator(booklist, 20)

    page = request.GET.get('page')
    books = paginator.get_page(page)

    return render(request, 'browse.html', {'books': books})
