from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

#Create functions

def newuser(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":"0"})
        db.session.commit()
    except:
        return False
    return login(username, password)

#Login and logout functions

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    session["csrf_token"] = secrets.token_hex(16)
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["username"]

#Get functions

def get_user_id():
    username = session["username"]
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_info = result.fetchone()
    user_id = user_info[0]
    return user_id
