from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from password import Password
from openhab import Openhab

app = Flask(__name__)
auth = HTTPBasicAuth()

openhab = Openhab()
password = Password()


@app.route('/locative', methods=['GET'])
@auth.login_required
def index():
    openhab.inform(username=auth.username().capitalize(), action=request.args.get('trigger'),
                   location=request.args.get('id'))
    return Response(status=200)


@app.route('/geofency', methods=['POST'])
@auth.login_required
def enter():
    openhab.inform(username=auth.username().capitalize(), action=request.form.get('entry'),
                   location=request.form.get('name'))
    return Response(status=200)


@auth.verify_password
def verify_password(username, user_password):
    return password.verify_password(username=username, password=user_password)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
