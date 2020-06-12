import boto3 as b3
import json
from dynamodb_json import json_util
from datetime import datetime, timezone
import uuid

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


def create_book(name, year, author, user_id):
    """Creates a book instance in dynamo and returns the created book"""

    created_date = datetime.now(timezone.utc).date()

    new_book = {
        'id': str(uuid.uuid1()),
        'user_id': str(user_id),
        'name': str(name),
        'year': str(year),
        'author': str(author),
        'created_at': str(created_date),
        'updated_at': str(created_date),
    }

    dynamo.put_item(
        TableName='books',
        Item=json.loads(json_util.dumps(new_book))
    )

    return new_book
