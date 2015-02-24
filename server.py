from flask import app, request
from flask import Flask
import database_helper
import json

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        return "Hello world!"


@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.args.get('email')
        password = request.args.get('password')
        firstname = request.args.get('firstname')
        familyname = request.args.get('familyname')
        gender = request.args.get('gender')
        city = request.args.get('city')
        country = request.args.get('country')
        return json.dumps(database_helper.sign_up(email, password, firstname, familyname, gender, city, country))

@app.route('/signin', methods=['GET'])
def sign_in():
    if request.method == 'GET':
        return json.dumps(database_helper.sign_in(request.args.get('email'), request.args.get('password')))



@app.route('/signout', methods=['GET'])
def sign_out():
    if request.method == 'GET':
        return json.dumps(database_helper.sign_out(request.args.get('token')))

@app.route('/changepassword', methods=['POST'])
def change_password():
    if request.method == 'POST':
        return json.dumps(database_helper.change_password(request.args.get('token'), request.args.get('oldpw'), request.args.get('newpw')))


@app.route('/getuserdatabyemail', methods=['GET'])
def get_user_data_by_email():
    if request.method == 'GET':
        return json.dumps(database_helper.get_user_data_by_email(request.args.get('token'), request.args.get('email')))

@app.route('/getuserdatabytoken', methods=['GET'])
def get_user_data_by_token():
    if request.method == 'GET':
        return json.dumps(database_helper.get_user_data_by_token(request.args.get('token')))

@app.route('/getusermessagesbytoken', methods=['GET'])
def get_user_messages_by_token():
    if request.method == 'GET':
        return json.dumps(database_helper.get_user_messages_by_token(request.args.get('token')))


@app.route('/getusermessagesbyemail', methods=['GET'])
def get_user_messages_by_email():
    if request.method == 'GET':
        return json.dumps(database_helper.get_user_messages_by_email(request.args.get('token'), request.args.get('email')))

@app.route('/postmessage', methods=['POST'])
def post_message():
    if request.method == 'POST':
        return json.dumps(database_helper.post_message(request.args.get('token'), request.args.get('message'), request.args.get('email')))

@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close_db()

if __name__ == '__main__':
    app.run()