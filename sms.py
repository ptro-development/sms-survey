from twilio.rest import Client

# TODO: put this into config
account_sid = "..."
auth_token = "..."
sender_number = "..."

client = Client(account_sid, auth_token)

def send(receiver_number, body):
    message = client.messages.create(body = body, from_= sender_number, to = receiver_number)
    return message.sid

def getInboundMessages():
    """ Message data
    ['AddressRetention', 'ContentRetention', 'Direction',
     'Status', 'TrafficType', 'account_sid', 'api_version',
     'body', 'date_created', 'date_sent', 'date_updated',
     'delete', 'direction', 'error_code', 'error_message',
     'feedback', 'fetch', 'from_', 'media', 'messaging_service_sid',
     'num_media', 'num_segments', 'price', 'price_unit',
     'sid', 'status', 'subresource_uris', 'to', 'update', 'uri']
    """
    messages = []
    for sms in client.messages.list():
        if sms.direction == "inbound":
            messages.append(sms)
            #print "From:" + sms.from_
            #print "Body:" + sms.body
            #print "---------------"
    return messages
