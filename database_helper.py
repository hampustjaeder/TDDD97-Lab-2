__author__ = 'mtr'

import sqlite3
from flask import g
import json, ast
import random, string


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


# Done
def close_db():
    get_db().close()


# Done - tested
def generate_token():
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(36))


# Done - tested (SQL inj protected)
def sign_in(email, password):
    c = get_db()
    res = c.execute("SELECT * FROM users WHERE email=:mail AND password=:pw LIMIT 1",  {"mail": email, "pw": password})
    res = res.fetchone()
    if not res:  # Not logged in
        return json.dumps({"success": False, "message": "Invalid email or password"})
    else:  # Logged in
        token = generate_token()
        c.execute("INSERT INTO loggedusers values(?, ?)", (email, token))
        return json.dumps({"success": True, "message": "You are now signed in", "data": token})


# Done - tested (SQL inj protected)
def sign_up(email, password, firstname, familyname, gender, city, country):
    c = get_db()
    res = c.execute("SELECT * FROM users WHERE email=:mail LIMIT 1", {"mail":email})
    res = res.fetchone()
    if not res:
        try:
            c.execute("INSERT INTO users values(?, ?, ?, ?, ?, ?, ?)", (email, password, firstname, familyname, gender, city, country))
            c.commit()
            return json.dumps({"success": True, "message": "Successfully created a new user."})
        except:
            c.rollback()
            return json.dumps({"success": False, "message": "Formdata not complete."})

    else:
        return json.dumps({"success": False, "message": "User already exists."})


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


# Done - tested (SQL inj protected)
def get_user_data_by_email(token, email):
    c = get_db()
    res = c.execute("SELECT * FROM loggedusers WHERE userID=:ID LIMIT 1", {"ID": token})
    res = res.fetchone()
    if res:
        data = c.execute("SELECT * FROM users WHERE email=:mail LIMIT 1", {"mail": email})
        data = data.fetchone()
        if not res:
            return json.dumps({"success": False, "message": "No such user."})
        else:
            return json.dumps({"success": True, "message": "User data retrieved.", "data": data})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})


# Done - tested (SQL inj protected)
def get_user_data_by_token(token):
    email = get_email_by_token(token).fetchone()[0]
    return get_user_data_by_email(token, email)


# Done - tested (SQL inj protected)
def get_user_messages_by_token(token):
    email = get_email_by_token(token).fetchone()
    print(email)
    return get_user_messages_by_email(token, email)


# Done - tested (SQL inj protected)
def get_user_messages_by_email(token, username):
    c = get_db()

    res = c.execute("SELECT * FROM loggedusers WHERE userID=:ID LIMIT 1", {"ID": token}).fetchone()
    if res:
        res = c.execute("SELECT * FROM users WHERE email=:mail", {"mail":username}).fetchone()
        if not res:
            return json.dumps({"success": False, "message": "No such user."})
        else:
            messageList=[];
            for row in c.execute("SELECT message FROM messages WHERE email=:mail", {"mail":username}):
                messageList.append(row)
            return json.dumps({"success": True, "message": "User messages retrieved.", "messages": messageList})

    else:
        return json.dumps({"success": False, "message": "You are not signed in."})


# Done - tested (SQL inj protected)
def post_message(token, message, username):
    c = get_db()
    res = get_email_by_token(token)
    #NEED TO Check fOR USER!!! (Can post to a user that doesnt exist.
    if res:
        try:
            c.execute("INSERT INTO messages values(?, ?)", (username, message))
            c.commit()
            return json.dumps({"success": True, "message": "Message posted"})
        except:
            c.rollback()
            return json.dumps({"success": False, "message": "ROLLBACK - No such user."})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})
