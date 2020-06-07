import boto3 as b3
import json
from dynamodb_json import json_util

REGION_NAME = 'us-east-1'

# Create DynamoClient
dynamo = b3.client('dynamodb', region_name='us-east-1')


def create_user(id, username, name, email, role, library):
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
