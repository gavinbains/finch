from flask import Flask, request
import requests
import json

# initialize flask
app = Flask(__name__)

# declare some constants
XPRING_HEADERS = {
    'Authorization': 'Bearer g280wombfhuxn5o2j6c54',
    'Content-Type': 'application/json',
}
XPRING_URL = "http://localhost:3000/v1"

IMMIGRANT_DATA = {
    'name': '',
    'alien_id': '',
    'date_of_birth': '',
    'det_center': '',
    'country_of_origin': '',
    'spoken_languages': '',
    'preferred_language': '',
    'written_language': '',
    'prev_council': ''
}

# default route
@app.route('/')
def index():
    return 'Hello World!'

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook_main():

    data = request.get_json(force=True)
    action = data['queryResult']['action']
    fulfillmentText = 'We are working on getting a solution...'


    print("~~~~~YOU HAVE GOTTEN A RESPONSE~~~~~~~~")
    print(action)

    if action == 'input.welcome':
        name = data['queryResult']['parameters']['name'][0]
        a_id = data['queryResult']['parameters']['alien_id'][0]
        IMMIGRANT_DATA['name'] = name
        IMMIGRANT_DATA['alien_id'] = a_id
        fulfillmentText = 'Hello {}! Nice to meet you. Everything will be ok. Would you like a lawyer to represent you?'.format(name)

        print('~~WELCOME VALUES:')
        print(name, a_id)

    elif action == 'input.request_lawyer':
        date_of_birth = data['queryResult']['parameters']['dob']
        det_center = data['queryResult']['parameters']['det_center']
        country_of_origin = data['queryResult']['parameters']['origin']
        IMMIGRANT_DATA['date_of_birth'] = date_of_birth
        IMMIGRANT_DATA['det_center'] = det_center
        IMMIGRANT_DATA['country_of_origin'] = country_of_origin
        fulfillmentText = 'Thank You. This will help a lot. I have a few more questions for you. Do you speak any other languages?'

        print('~~LAWYERS CHOICE VALUES:')
        print(date_of_birth, det_center, country_of_origin)

    elif action == 'input.question_6':
        spoken_languages = data['queryResult']['parameters']['spoken_language']
        IMMIGRANT_DATA['spoken_languages'] = spoken_languages
        fulfillmentText = 'Great! Next question. What language would you like to be interviewed in?'

        print('~~LANGUAGES SPOKEN:')
        print(spoken_languages)

    elif action == 'input.question_7':
        preferred_language = data['queryResult']['parameters']['preferred_language']
        IMMIGRANT_DATA['preferred_language'] = preferred_language
        fulfillmentText = 'We will find someone to interview you in {}. Next question. In which languages can you read?'.format(preferred_language)

        print('~~PREFERRED LANGUAGE:')
        print(preferred_language)

    elif action == 'input.question_8':
        written_language = data['queryResult']['parameters']['written_language']
        IMMIGRANT_DATA['written_language'] = written_language
        fulfillmentText = 'Great! All this information will be sent to a lawyer who will help you. Next Question. Have you ever spoken with or had an attorney represent you before the immigration court?'

        print('~~WRITTEN LANGUAGE:')
        print(written_language)

    elif action == 'input.question_9':
        prev_council = data['queryResult']['parameters']['prev_council']
        IMMIGRANT_DATA['prev_council'] = prev_council
        fulfillmentText = 'Thank you for your time. We will now send this information to a group of lawyers who will try and help you. we hope to help you soon.'

        print('~PREVIOUS COUNCIL?')
        print(prev_council)

    full = True
    for key in IMMIGRANT_DATA:
        full &= IMMIGRANT_DATA[key]!=''

    print("FULL? {}".format(full))
    print(IMMIGRANT_DATA)
    if(full):
        print("YOUR IMMIGRANT DATA IS FULL")

    return {'fulfillmentText': fulfillmentText}


# create a route for getAccount
@app.route('/getAccount')
def getAccount():
    response = requests.get(XPRING_URL + '/accounts/rwdy5m8YSYuvWcLxtPpm5ute7neWjA5Hr7/info')
    return response.json()

# create a route for reimburse
@app.route('/reimburse')
def reimburse():
    data = '{"payment": {"source_address": "rwdy5m8YSYuvWcLxtPpm5ute7neWjA5Hr7","source_amount": {"value": "2","currency": "XRP"},"destination_address": "rJE3LVb4JjzCqNdZqKEwQuyw2Dev6sQQw","destination_amount": {"value": "2","currency": "XRP"}},"submit": true}'
    response = requests.post(url + '/payments', headers=XPRING_HEADERS, data=data)
    return response.json()

# create a route for laywerfunds
@app.route('/lawyerfunds')
def lawyerfunds():
    return 'Hello HookWorld!'

# run the app
if __name__ == '__main__':
   app.run()
