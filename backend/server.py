from flask import Flask
import requests

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
    return response.json()

# create a route for laywerfunds
@app.route('/lawyerfunds')
def lawyerfunds():
    return 'Hello HookWorld!'

# run the app
if __name__ == '__main__':
   app.run()
