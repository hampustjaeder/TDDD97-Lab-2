__author__ = 'mtr'

import sqlite3
from flask import g
import json, ast


DATABASE = 'database.db'

# Done
def connect_db():
    return sqlite3.connect("database.db")

# Done
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
        db.text_factory = sqlite3.OptimizedUnicode
    return db

#       1 User table with status if online/offline, 1 table for messages(?)
#       1 User table, 1 LoggedUsers table
def init():
    c = get_db()
    #Users
    c.execute("drop table if exists users")
    c.execute("create table users (email text, password text, firstname text, familyname text, gender text, city text, country text, messages text)")
    #Loggedusers
    c.execute("drop table if exists loggedusers")
    c.execute("create table loggedusers (email text, userID text)")
    c.commit()
    print("Database Initialized")

    su = sign_up('email', 'password1', 'firstname', 'familyname', 'gender', 'linkoping', 'country', 'messages')
    si = sign_in('email', 'password1')
    res = c.execute("SELECT * FROM loggedusers WHERE email='email' AND userID='1337' LIMIT 1")
    res = res.fetchone()
    print("Loggeduser table: ", res)
    res = c.execute("SELECT * FROM users WHERE email='email' LIMIT 1")
    res = res.fetchone()
    print("User table: ", res)

    cp = change_password('1337', 'password1', 'hejsan123')
    print("Change_password: ",cp)
    res = c.execute("SELECT * FROM users WHERE email='email' LIMIT 1")
    res = res.fetchone()
    print("User table: ", res)
    print(get_user_data_by_email('1337', 'email'))

    so = sign_out('1337')


# Done
def close_db():
    get_db().close()


# Not Done
def generate_token():
    return '1337';


# Done - tested (SQL inj protected)
def sign_in(email, password):
    c = get_db()
    res = c.execute("SELECT * FROM users WHERE email=:mail AND password=:pw LIMIT 1",  {"mail": email, "pw": password})
    res = res.fetchone()
    if not res:  # Not logged in
        return json.dumps({"success": False, "message": "Invalid email or password"})
    else:  # Logged in
        token = generate_token()
        c.execute("INSERT INTO loggedusers VALUES (?, ?)", (email, token))
        return json.dumps({"success": True, "message": "You are now signed in"})#, "data": token})
    return None


# Done - tested (SQL inj protected)
def sign_up(email, password, firstname, familyname, gender, city, country, messages):
    c = get_db()
    res = c.execute("SELECT * FROM users WHERE email=:mail LIMIT 1", {"mail":email})
    res = res.fetchone()
    if not res:
        try:
            c.execute("INSERT INTO users values(?, ?, ?, ?, ?, ?, ?, ?)", (email, password, firstname, familyname, gender, city, country, messages))
            c.commit()
            return json.dumps({"success": True, "message": "Successfully created a new user."})
        except:
            c.rollback()
            return json.dumps({"success": False, "message": "Formdata not complete."})

    else:
        return json.dumps({"success": False, "message": "User already exists."})
    return None


# Done - tested (SQL inj protected)
def sign_out(token):
    c = get_db()
    res = c.execute("SELECT * FROM loggedusers WHERE userID=:ID LIMIT 1", {"ID": token})
    res = res.fetchone()
    if res:
        try:
            c.execute("DELETE FROM loggedusers WHERE userID=:ID", {"ID": token})
            c.commit()
            return json.dumps({"success": True, "message": "Successfully signed out"})
        except:
            c.rollback()
            return json.dumps({"success": False, "message": "Failed to sign out"})

    else:
        return json.dumps({"success": False, "message": "You are not signed in."})
    return None


# Done - tested (SQL inj protected)
def get_email_by_token(token):
    c = get_db()
    return c.execute("SELECT email FROM loggedusers WHERE userID=:ID", {"ID": token})


# Done - tested (SQL inj protected)
def change_password(token, old_password, new_password):
    c = get_db()
    username = get_email_by_token(token).fetchone()

    if username:
        pw = c.execute("SELECT password FROM users WHERE email IS ? LIMIT 1", username)
        pw = pw.fetchone()[0]
        if pw == old_password:
            try:
                c.execute("UPDATE users SET password=:npw WHERE email=:mail", {"npw":new_password, "mail":username[0]})
                c.commit()
                return json.dumps({"success": True, "message": "Password changed."})
            except:
                c.rollback()
                return json.dumps({"success": False, "message": "Rollback, Password not changed."})
        else:
            return json.dumps({"success": False, "message": "Wrong password."})

    else:
        return json.dumps({"success": False, "message": "You are not signed in."})


# Working on
def get_user_data_by_email(token, email):
    c = get_db()
    # if loggedInUsers(token) != null
    res = c.execute("SELECT * FROM loggedusers WHERE userID=:ID LIMIT 1", {"ID": token})
    res = res.fetchone()
    if res:
        messages = c.execute("SELECT * FROM users WHERE email=:mail LIMIT 1", {"mail": email})
        res = messages.fetchone()
        if not res:
            # User not signed up
            return json.dumps({"success": False, "message": "No such user."})
        else:
            # User signed up
            return json.dumps({"success": True, "message": "User data retrieved.", "data": "data"})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})


# Not Done
def get_user_data_by_token(token):
    email = get_emailbytoken(token)
    return get_user_data_by_email(token, email)


# Not Done
def get_user_messages_by_token(token):
    email = get_emailbytoken(token)
    return get_user_messages_by_email(token, email)


# Not Done
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


# Not Done
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
