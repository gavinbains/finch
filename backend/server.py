from flask import Flask
import requests


# declare some constants
XPRING_HEADERS = {
    'Authorization': 'Bearer g280wombfhuxn5o2j6c54',
    'Content-Type': 'application/json',
}
XPRING_URL = "http://localhost:3000/v1"

app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'
# create a route for webhook
@app.route('/webhook')
def hello():
    return 'Hello Hook!'


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
