from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import users
import runroutes
from db import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/create", methods=["GET","POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    length = request.form["length"]
    if runroutes.create(name, type, length):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a new route")

@app.route("/newuser", methods=["GET","POST"])
def newuser():
    if request.method == "GET":
        return render_template("newuser.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.newuser(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")

@app.route("/browseroutes")
def browseroutes():
    sql = "SELECT id, name, type, length FROM routes"
    result = db.session.execute(sql)
    routes = result.fetchall()
    db.session.commit()
    return render_template("browseroutes.html", routes=routes)

@app.route("/newroute")
def newroute():
    return render_template("newroute.html")

@app.route("/reviewroute")
def reviewroute():
    return render.template("reviewroute.html")
