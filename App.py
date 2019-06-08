from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "user1": generate_password_hash("PASSWORD"),
    "user2": generate_password_hash("PASSWORD")
}

enter_leave = {
    "enter": "ON",
    "leave": "OFF"
}


@app.route('/', methods=['GET'])
@auth.login_required
def index():
    action = request.args.get('trigger')
    location = request.args.get('id')
    print(f"{auth.username().capitalize()} : {action}  -> {location}")
    if location == 'test':
        print("Test Request")
    # else:
        headers = {'content-type': 'text/plain', 'Accept': 'application/json'}
        url = f"http://192.168.10.5:8080/rest/items/Anwesenheit_{auth.username().capitalize()}"
        requests.post(url, data=enter_leave.get(action), headers=headers)

    return Response(status=200, mimetype='application/json')


@auth.verify_password
def verify_password(username, password):
    print(username, password)
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
