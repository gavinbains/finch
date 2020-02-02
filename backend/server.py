from flask import Flask, jsonify, render_template
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Use the application default credentials
cred = credentials.Certificate("/Users/gbains/dev/finch/backend/finch-c2cd142dfd08.json")
firebase_admin.initialize_app(cred, {
  'projectId': "finch-b50f9",
})

db = firestore.client()

# initialize flask
app = Flask(__name__)

# declare some constants
XPRING_HEADERS = {
    'Authorization': 'Bearer g280wombfhuxn5o2j6c54',
    'Content-Type': 'application/json',
}
XPRING_URL = "http://localhost:3000/v1"
sourceAddr = "rwdy5m8YSYuvWcLxtPpm5ute7neWjA5Hr7"
destAddr = "rJE3LVb4JjzCqNdZqKEwQuyw2Dev6sQQw"
# default route
@app.route('/')
def index():
    return 'Hello World!'

# create a route for webhook
@app.route('/wh_initial')
def hello():
    # req = request.get_json(force=True)
    # print(req)
    return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for getAccount
@app.route('/getAccount')
def getAccount():
    response = requests.get(XPRING_URL + '/accounts/' + sourceAddr + '/info')
    return response.json()

# create a route for reimburse
@app.route('/reimburse')
def reimburse():
    data = '{"payment": {"source_address": ' + sourceAddr + ',"source_amount": {"value": "2","currency": "XRP"},"destination_address": ' + destAddr + ',"destination_amount": {"value": "2","currency": "XRP"}},"submit": true}'
    response = requests.post(XPRING_URL + '/payments', headers=XPRING_HEADERS, data=data)
    print("PAYMENT MADE")
    return response.json()

# create a route for laywerfunds
@app.route('/lawyerfunds')
def lawyerfunds():
    return 'Hello HookWorld!'

# create a route for laywerfunds
@app.route('/addImmigrant')
# name, alien_id, date_of_birth, country_of_birth, detention_center, spoken_language, written_language, previous_represented_by_lawyer
def addImmigrant():
    doc_ref = db.collection(u'immigrants').document(u'alovelace')
    doc_ref.set({
        u'name': u'Ada Lovelace',
        u'alien_id': u'1234',
        u'date_of_birth': u'1815',
        u'country_of_birth': u'Canada',
        u'detention_center': u'1234',
        u'spoken_language': u'English',
        u'written_language': u'English',
        u'previous_represented_by_lawyer': False,
    })
    return 'ADDED immigrants'

# create a route for laywerfunds
@app.route('/getImmigrants')
# name, alien_id, date_of_birth, country_of_birth, detention_center, spoken_language, written_language, previous_represented_by_lawyer
def getImmigrants():
    users_ref = db.collection(u'immigrants')
    docs = users_ref.stream()
    ans = []
    for doc in docs:
        ans.append(doc.to_dict())
    print(ans)
    return render_template('lawyers.html', immigrants=ans)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

# run the app
if __name__ == '__main__':
   app.run()
