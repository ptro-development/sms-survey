import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('user')
survey_table = dynamodb.Table('survey')

def getUser(number=None):
    if number:
        # print number
        items = user_table.query(
            KeyConditionExpression=Key('number').eq(number))['Items']
        if items:
            return items[0]
        else:
            return None
    else:
        return user_table.scan()['Items']

def postUser(number, email, httpurl, notification_choice):
    user_table.put_item(
        Item = {
            'number': number,
            'email': email,
            'httpurl': httpurl,
            'notification': notification_choice
        })

def getSurvey():
    return survey_table.scan()['Items']

def postSurvey(number, question, keyword):
    survey_table.put_item(
        Item = {
            'number': number,
            'question': question,
            'keyword': keyword,
        })

def updateSurvey(number, keyword, answer):
    items = survey_table.scan(
        FilterExpression=Attr('number').eq(number) & Attr('keyword').eq(keyword))['Items']
    # print "items:" + str(items)
    # print "number:" + str(number)
    # print "keyword:" + str(keyword)
    if len(items) == 1:
        survey_table.update_item(
            Key = {
                'number': number,
                'question': items[0].get('question')
            },
            UpdateExpression = 'SET answer = :val',
            ExpressionAttributeValues = {
                ':val': answer
            })
        return survey_table.get_item(
            Key = {
                'number': number,
                'question': items[0].get('question')
            })['Item']
    else:
        return None
