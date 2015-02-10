__author__ = 'mtr'

import sqlite3
from flask import g
import json


DATABASE = 'database.db'


def connect_db():
    return sqlite3.connect("database.db")


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

#       1 User table with status if online/offline, 1 table for messages.
def init():
    c = get_db()
    #Users
    c.execute("drop table if exists users")
    c.execute("create table users (email text, password text, firstname text, familyname text, gender text, city text, country text, messages text)")
    #Loggedusers
    c.execute("drop table if exists loggedusers")
    c.execute("create table loggedusers (email text, userID text)")

  #  c.execute("INSERT INTO users VALUES ('email', 'password', 'firstname', 'familyname', 'gender', 'linkoping', 'country', 'messages')")
    c.commit()
    print("Database Initialized")
    sign_up('email', 'password', 'firstname', 'familyname', 'gender', 'linkoping', 'country', 'messages')
    print("Users signed up")
    sign_in('email', 'password')
    res = c.execute("SELECT * FROM loggedusers WHERE email='email' AND userID='token' LIMIT 1")
    #res = c.execute("SELECT * FROM users WHERE email='email' AND password='password' LIMIT 1")
    res = res.fetchone()
    print(res)

def close_db():
    get_db().close()


def sign_in(email, password):
     c = get_db()
     res = c.execute("SELECT * FROM users WHERE email='"+email+"' AND password='"+password+"' LIMIT 1")
     res = res.fetchone()
     if not res:
        # Not logged in
        return json.dumps({"success": False, "message": "Invalid email or password"})
     else:
        # Logged in
        #Generate TOKEN here...
        c.execute("INSERT INTO loggedusers VALUES ('email', 'token')")
        return json.dumps({"success": True, "message": "You are now signed in"})#, "data": token})
     return None
    #removed on purpose


def sign_up(emil, password, firstname, familyname, gender, city, country, messages):
    c = get_db()
    #if user[email] == null (no such user)
    res = c.execute("INSERT INTO users values(email, password, firstname, familyname, gender, city, country, messages)")
    res = res.fetchone()
    if not res:
        # User not signed up
        return json.dumps({"success": False, "message": "Formdata not complete."})
    else:
        # User signed up
        c.commit()
        return json.dumps({"success": True, "message": "Successfully created a new user."})
    return None
    #else
        #return json.dumps({"success": False, "message": "User already exists."})


def sign_out(token): #token
    c = get_db()
    # if loggedInUsers(token) != null
    res = c.execute("DELETE FROM loggedusers WHERE userID=token")
    #res = res.fetchone()
    #if not res:
    # User signed out
    c.commit()
    return json.dumps({"success": True, "message": "Successfully signed out."})
     #else:
        # User not signed out
        #return json.dumps({"success": False, "message": "You are not signed in."})
     #return None


def get_emailbytoken(token):
    c = get_db()
    return c.execute("SELECT email FROM loggedusers WHERE userID=token")


def change_password(token, old_password, new_password):
    c = get_db()
    #Update IF old_password is correct!
    # if loggedInUsers(token) != null
    username = get_emailbytoken(token)
    res = c.execute("UPDATE users SET password = new_password WHERE email=username")
    res = res.fetchone()
    if not res:
        # User not signed up
        return json.dumps({"success": False, "message": "Wrong password."})
    else:
        # User signed up
        c.commit()
        return json.dumps({"success": True, "message": "Password changed."})
    return None
    #else
    #return json.dumps({"success": False, "message": "You are not signed in."})


def get_user_data_by_email(token, email):
    c = get_db()
    # if loggedInUsers(token) != null
    messages = c.execute("SELECT messages FROM users WHERE email='"+email+"")
    res = messages.fetchone()
    if not res:
        # User not signed up
        return json.dumps({"success": False, "message": "No such user."})
    else:
        # User signed up
        return json.dumps({"success": True, "message": "User data retrieved."})#, "data": messages})
    return None
    #else
    #return json.dumps({"success": False, "message": "You are not signed in."})


def get_user_data_by_token(token):
    email = get_emailbytoken(token)
    return get_user_data_by_email(token, email)


def get_user_messages_by_token(token):
    email = get_emailbytoken(token)
    return get_user_messages_by_email(token, email)


def get_user_messages_by_email(token, email):
    c = get_db()
    # if loggedInUsers(token) != null
    messages = c.execute("SELECT messages FROM users WHERE email='"+email+"")
    res = messages.fetchone()
    if not res:
        # User not signed up
        return json.dumps({"success": False, "message": "No such user."})
    else:
        # User signed up
        return json.dumps({"success": True, "message": "User messages retrieved."})#, "data": messages})
    return None
    #else
    #return json.dumps({"success": False, "message": "You are not signed in."})


def post_message(token, message, username):
    c = get_db()
    #Update     if get_emailbytoken(token) != null
    username = get_emailbytoken(token)
    res = c.execute("UPDATE users SET messages = message WHERE email=username")
    res = res.fetchone()
    if not res:
        # No such user
        return json.dumps({"success": False, "message": "No such user."})
    else:
        # Message posted
        c.commit()
        return json.dumps({"success": True, "message": "Message posted"})
    return None
    #else
        #return json.dumps({"success": False, "message": "You are not signed in."})
