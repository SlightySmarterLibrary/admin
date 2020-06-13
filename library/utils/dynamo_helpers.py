import boto3 as b3
import json
from dynamodb_json import json_util
from datetime import datetime, timezone
import uuid
import qrcode
from .s3_helpers import upload_book_qr_code
from boto3.dynamodb.conditions import Key, Attr

REGION_NAME = 'us-east-1'

# Create DynamoClient
dynamo = b3.client('dynamodb', region_name=REGION_NAME)
s3 = b3.client('s3', region_name=REGION_NAME)


def create_user(id, username, name, email, role, library):
    """Creates a user instance in dynamo and returns the created user"""
    new_user = {
        'id': str(id),
        'username': str(username),
        'name': str(name),
        'email': str(email),
        'role': str(role),
        'library': str(library),
    }

    dynamo.put_item(
        TableName='users',
        Item=json.loads(json_util.dumps(new_user))
    )

    return new_user


def create_book(name, year, author, genre, isbn, user_id):
    """Creates a book instance in dynamo and returns the created book"""

    book_id = str(uuid.uuid1())
    created_date = datetime.now(timezone.utc).date()
    qr = qrcode.make(book_id)
    qr_code = upload_book_qr_code(id=book_id, qr_code=qr, user_id=str(user_id))

    new_book = {
        'id': book_id,
        'user_id': str(user_id),
        'name': str(name),
        'year': str(year),
        'author': str(author),
        'created_at': str(created_date),
        'updated_at': str(created_date),
        'qr_code': qr_code,
        'genre': genre,
        'isbn': isbn
    }

    dynamo.put_item(
        TableName='books',
        Item=json.loads(json_util.dumps(new_book))
    )

    return new_book


def get_books(user_id=None):
    queryCondition = "user_id = :user_id"
    queryAttributes = {
        ':user_id': user_id,
    }
    dynamodb = b3.resource('dynamodb', region_name="us-east-1")
    books = dynamodb.Table('books')

    response = books.query(
        IndexName="user_id-index",
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    return json_util.loads(response['Items'])
