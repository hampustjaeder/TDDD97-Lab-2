from flask import app, request
from flask import Flask
import database_helper

app = Flask(__name__)
app.debug = True


@app.route('/signup', methods=['POST'])
def sign_up():
    #if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    messages = []
    result = database_helper.sign_up(email, password, firstname, familyname, gender, city, country, messages)
    return result

@app.route('/signin', methods=['POST'])
def sign_in():
    return database_helper.sign_in(request.form['email'], request.form['password'])

@app.route('/signout', methods=['POST'])
def sign_out(token): #token=''
    #if request.method == 'POST':
    return database_helper.sign_out(token)

@app.route('/changepassword', methods=['POST'])
def change_password(token):
    #if request.method == 'POST':
    return change_password(token, request.form['oldpw'], request.form['newpw'])

@app.route('/getuserdatabyemail', methods=['GET'])
def get_user_data_by_email(token, email):
    #if request.method == 'GET':
    return database_helper.get_user_data_by_email(token, email)

@app.route('/getuserdatabytoken', methods=['GET'])
def get_user_data_by_token(token):
    #if request.method == 'GET':
    return database_helper.get_user_data_by_token(token)

@app.route('/getusermessagesbytoken', methods=['GET'])
def get_user_messages_by_token(token):
    #if request.method == 'GET':
    return database_helper.get_user_messages_by_token(token)

@app.route('/getusermessagesbyemail/<token>/<email>', methods=['GET'])
def get_user_messages_by_email(token, email):
    #if request.method == 'GET':
    return database_helper.get_user_messages_by_email(token, email)

@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close_db()

if __name__ == '__main__':
    with app.app_context():
        database_helper.init()
