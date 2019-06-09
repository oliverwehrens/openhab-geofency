from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
import requests
import hashlib

app = Flask(__name__)
auth = HTTPBasicAuth()

enter_leave = {
    "enter": "ON",
    "leave": "OFF"
}


@app.route('/', methods=['GET'])
@auth.login_required
def index():
    action = request.args.get('trigger')
    location = request.args.get('id')
    config_file = open('openhab-config.txt', 'r', encoding='utf-8')
    openhab_base_url = config_file.read().rstrip('\n')
    config_file.close()

    print(f"{auth.username().capitalize()} : {action}  -> {location}")
    headers = {'content-type': 'text/plain', 'Accept': 'application/json'}
    url = f"{openhab_base_url}/rest/items/Presence_{auth.username().capitalize()}_{location}"
    requests.post(url, data=enter_leave.get(action), headers=headers)

    return Response(status=200, mimetype='application/json')


@auth.verify_password
def verify_password(username, password):
    users = {}
    password_file = open('users.txt', 'r', encoding='utf-8')
    for line in password_file.readlines():
        entry = line.rstrip('\n').split(" ")
        users[entry[0]] = entry[1]
    password_file.close()
    if username in users:
        encrypted_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        return encrypted_password == users.get(username)
    return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
