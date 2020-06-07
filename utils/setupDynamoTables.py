import boto3

REGION_NAME = 'us-east-1'

# Create DynamoClient
dynamo = boto3.client('dynamodb', region_name='us-east-1')


def format_attr(name, attribute_type):
    return {
        'AttributeName': name,
        'AttributeType': attribute_type
    }


def attributes(attribs):
    formatted_attributes = map(lambda x: format_attr(
        name=x[0], attribute_type=x[1]), attribs)

    return list(formatted_attributes)


def format_schema(name, schema_type):
    return {
        'AttributeName': name,
        'KeyType': schema_type
    }


def schema(attribs):
    formatted_attributes = map(lambda x: format_schema(
        name=x[0], schema_type=x[1]), attribs)

    return list(formatted_attributes)


def create_table(name, attribs, keySchema):
    try:
        dynamo.create_table(
            TableName=name,
            AttributeDefinitions=attributes(attribs=attribs),
            KeySchema=schema(attribs=keySchema),
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            },
        )
        dynamo.get_waiter('table_exists').wait(TableName=name)
    except dynamo.exceptions.ResourceInUseException:
        pass
    except Exception as e:
        print(f"Error creating table: {name}")
        print(e)

# Create Tables


create_table(name="books", attribs=[
             ['id', 'S'], ['name', 'S']], keySchema=[['id', 'HASH'], ['name', 'RANGE']])
create_table(name="users", attribs=[
             ['id', 'S'], ['name', 'S']], keySchema=[['id', 'HASH'], ['name', 'RANGE']])
create_table(name="reservations", attribs=[
             ['id', 'S'], ['user_id', 'S']], keySchema=[['id', 'HASH'], ['user_id', 'RANGE']])
create_table(name="transactions", attribs=[
             ['id', 'S']], keySchema=[['id', 'HASH']])
create_table(name="checkouts", attribs=[
             ['id', 'S']], keySchema=[['id', 'HASH']])
create_table(name="waiting_lists", attribs=[
             ['id', 'S'], ['book_id', 'S']], keySchema=[['id', 'HASH'], ['book_id', 'RANGE']])
