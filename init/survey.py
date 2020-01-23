import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='survey',
    KeySchema=[
        {
            'AttributeName': 'number',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'question',
            'KeyType': 'RANGE'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'number',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'question',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='survey')

# Print out some data about the table.
print(table.item_count)
