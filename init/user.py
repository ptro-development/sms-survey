import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='user',
    KeySchema=[
        {
            'AttributeName': 'number',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'email',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'number',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='user')

# Print out some data about the table.
print(table.item_count)
