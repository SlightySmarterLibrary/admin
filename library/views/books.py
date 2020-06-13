from django.views.generic import FormView, TemplateView
from library.utils.dynamo_helpers import create_book
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import boto3
from library.forms import CreateBookForm
from django.shortcuts import resolve_url
from library.utils.dynamo_helpers import get_books


def index(request):
    books = get_books(str(request.user.id))

    return render(request, 'index.html')


class CreateBook(FormView):
    template_name = 'library/books/create.html'
    form_class = CreateBookForm

    def get_success_url(self):
        return resolve_url('/')

    def form_valid(self, form):
        try:
            created_book = create_book(
                form.book['name'],
                form.book['year'],
                form.book['author'],
                form.book['genre'],
                form.book['isbn'],
                user_id=self.request.user.id)
        except Exception as e:
            print(e)
            form.errors['name'] = form.error_class(
                [f"We couldn't save this book. {e}"]
            )

            return self.form_invalid(form)

        return super().form_valid(form)


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
