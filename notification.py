import web

# TOD: put into config
web.config['sendmail_path'] = "/usr/sbin/sendmail"
sender_email="no-reply@survey.com"
email_headers=({'User-Agent': 'webpy.sendmail', 'X-Mailer': 'webpy.sendmail',})

def send_thanks(user, question, answer):
    sort_question = None
    if question.find('?') != -1:
        sort_question = question.split("?")[0] + "?"
    else:
        sort_question = question
    message = "Thanks for your answer to our survey quesion - %s with %s" % (
        sort_question, answer)
    send_message(user, message, 'Survey thanks')

def send_message(user, message, subject=None):
    # sending email
    # print "User:" + str(user)
    notification = user.get('notification')
    if notification.find("Email") != -1:
        # doing email
        receiver_email = user.get('email')
        web.sendmail(sender_email, receiver_email, subject, message, headers=email_headers)
        pass
    elif notification.find("HTTP") != -1:
        # doing post
        httpurl = user.get('httpurl')
        number = user.get('number')
        print "Fake post to user Number:%s URL:%s Message:%s" % (number, httpurl, message)
        pass
    else:
        # nothing to do
        pass
