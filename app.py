from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
#    sql = "SELECT id, password FROM users WHERE username=:username"
#    result = db.session.execute(sql, {"username":username})
#    user = result.fetchone()
#    if not user:
#        print("not ok")
#    else:
#        hash_value = user.password
#    if check_password_hash(hash_value,password):
#        print("ok")
#    else:
#        print("not ok")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    length = request.form["length"]
    sql = "INSERT INTO routes (name, type, length, created_at) VALUES (:name, :type, :length, NOW())"
    result =  db.session.execute(sql, {"name":name, "type":type, "length":length})
    db.session.commit()
    return redirect("/")

#@app.route("/newuser", methods=["POST"])
#def newuser():
#    username = request.form["username"]
#    password = request.form["password"]
#    hash_value = generate_password_hash(password)
#    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
#    db.session.execute(sql, {"username":username, "password":hash_value})
#    db.session.commit()
#    return render_template("/index")
#
@app.route("/browseroutes")
def browseroutes():
    sql = "SELECT id, name, type, length FROM routes"
    result = db.session.execute(sql)
    routes = result.fetchall()
    return render_template("browseroutes.html", routes=routes)

@app.route("/modifyroutes")
def modifyroutes():
    return render_template("modifyroutes.html")
