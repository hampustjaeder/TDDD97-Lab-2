from flask import app, request
from flask import Flask
import database_helper

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/signup')
def sign_up():
    email = request.args.get('email')
    password = request.args.get('password')
    firstname = request.args.get('firstname')
    familyname = request.args.get('familyname')
    gender = request.args.get('gender')
    city = request.args.get('city')
    country = request.args.get('country')
    return database_helper.sign_up(email, password, firstname, familyname, gender, city, country)

@app.route('/signin')
def sign_in():
    return database_helper.sign_in(request.args.get('email'), request.args.get('password'))

@app.route('/signout')
def sign_out():
    return database_helper.sign_out(request.args.get('token'))

@app.route('/changepassword')
def change_password():
    return database_helper.change_password(request.args.get('token'), request.args.get('oldpw'), request.args.get('newpw'))

@app.route('/getuserdatabyemail')
def get_user_data_by_email():
    return database_helper.get_user_data_by_email(request.args.get('token'), request.args.get('email'))

@app.route('/getuserdatabytoken')
def get_user_data_by_token():
    return database_helper.get_user_data_by_token(request.args.get('token'))

@app.route('/getusermessagesbytoken')
def get_user_messages_by_token():
    return database_helper.get_user_messages_by_token(request.args.get('token'))

@app.route('/getusermessagesbyemail')
def get_user_messages_by_email():
    return database_helper.get_user_messages_by_email(request.args.get('token'), request.args.get('email'))

@app.route('/postmessage')
def post_message():
    return database_helper.post_message(request.args.get('token'), request.args.get('message'), request.args.get('email'))

@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close_db()

if __name__ == '__main__':
    app.run()