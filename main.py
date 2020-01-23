import web
import model
import sms
import notification

urls = (
    '/', 'Index',
    '/user', 'User',
    '/user_survey', 'UserSurvey',
    '/sms_message', 'SmsMessage',
)

t_globals = {"datestr": web.datestr}
render = web.template.render("templates", base="base", globals=t_globals)

class Index:

    def GET(self):
        users_details = model.getUser()
        users_surveys = model.getSurvey()
        return render.index(users_details, users_surveys)

class User:

    form = web.form.Form(
        web.form.Textbox("number", web.form.notnull, size=30, description="Primary survey's phone number:"),
        web.form.Textbox("email", web.form.notnull, size=30, description="Secondary notifications by Email Address:"),
        web.form.Textbox("httpurl", web.form.notnull, size=100, description="Secondary notifications by HTTP POST url:"),
        web.form.Dropdown("notification", args=["Email address", "HTTP post url" ], value="Email address", description="Select secondary notification channel:"),
        web.form.Button("Submit", type="submit", description="Register"),)

    def GET(self):
        form = self.form()
        return render.user(form)

    def POST(self):
        form = self.form()
        data = web.input(_method='post')
        # not defined yet ...
        # form.validates()
        model.postUser(data.number, data.email, data.httpurl, data.notification)
        raise web.seeother("/")

class UserSurvey:

    users_numbers = [user.get('number') for user in model.getUser()]
    if not users_numbers:
        users_numbers = ["No numbers yet"]
    form = web.form.Form(
        web.form.Textbox("question", web.form.notnull, size=60, description="Question for user:"),
        web.form.Textbox("keyword", web.form.notnull, size=10, description="Required SMS response keyword:"),
        web.form.Dropdown("number", args=users_numbers, value=users_numbers[0], description="User mobile number:"),
        web.form.Button("Submit", type="submit", desctiprion="Ask user"),)

    def GET(self):
        form = self.form()
        return render.survey(form)
        
    def POST(self):
        form = self.form()
        # not defined yet ...
        # form.validates()
        data = web.input(_method='post')
        data.question += " Please, respond with %s:yes or %s:no thank you." % (
            data.keyword.lower(), data.keyword.lower())
        model.postSurvey(data.number, data.question, data.keyword.lower())
        sms.send(data.number, data.question)    
        raise web.seeother("/")

class SmsMessage:


    def GET(self):
        messages = sms.getInboundMessages()
        return render.sms_message(messages)

    def POST(self):
        """ Example of incoming message send by Twilio:
       Data from post:<Storage {'Body': u'PCKEYBOARD:YES', 'MessageSid': u'SMcb0e9652e927ef24f391a4824af2b766', 'FromZip': u'', 'From': u'+42190.....', 'SmsMessageSid': u'SMcb0e9652e927ef24f391a4824af2b766', 'AccountSid': u'ACb8209b47e69d92d50..........', 'FromCity': u'', 'ApiVersion': u'2010-04-01', 'To': u'+15742......', 'FromCountry': u'SK', 'NumMedia': u'0', 'ToZip': u'46951', 'ToCountry': u'US', 'NumSegments': u'1', 'SmsStatus': u'received', 'SmsSid': u'SMcb0e9652e927ef24f391a4824af2b766', 'ToCity': u'MACY', 'FromState': u'', 'ToState': u'IN'}>
18.206.172.64:41120 - - [22/Jan/2020 13:47:45]  
        """
        updated_item = None
        data = web.input(_method='post')
        body = str(data.Body).lower()
        # test valid response body and update survey
        if body.find(":yes") != -1 or body.find(":no") != -1: 
            keyword, answer = body.split(":")
            updated_item = model.updateSurvey(str(data.From), keyword, answer)
            # send notification based on preferences
            user = model.getUser(str(data.From))
            if updated_item and user:
                notification.send_thanks(
                    user, updated_item.get('question'), updated_item.get('answer')) 
        return "OK"

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
