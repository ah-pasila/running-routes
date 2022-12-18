from flask import Flask, redirect, render_template, request, session, make_response
from app import app
from db import db
import secrets
import users
import runroutes
import maps
import reviews

#Navigation and user functions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newuser", methods=["GET", "POST"])
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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Wrong username or password")

@app.route("/browsepersonal", methods=["GET", "POST"])
def browsepersonal():
    id = users.get_user_id()
    times = runroutes.get_route_times_by_user(id)
    routes = runroutes.get_routes_by_user(id)
    reviewlist = reviews.get_reviews_by_user(id)
    return render_template("browsepersonal.html", times=times, routes=routes, reviewlist=reviewlist)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#Route functions

@app.route("/newroute")
def newroute():
    return render_template("newroute.html")

@app.route("/createroute", methods=["GET", "POST"])
def createroute():
    name = request.form["name"]
    type = request.form["type"]
    length = request.form["length"]
    coordinates = request.form["coordinates"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    elif runroutes.create_route(name, type, length, coordinates):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a new route")

@app.route("/browseroutes")
def browseroutes():
    routes = runroutes.get_routes()
    return render_template("browseroutes.html", routes=routes)

#Map functions

@app.route("/newmap")
def newmap():
    routes = runroutes.get_route_names()
    return render_template("newmap.html", routes=routes)

@app.route("/uploadmap", methods=["GET", "POST"])
def uploadmap():
    routename = request.form["routename"]
    file = request.files["file"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    elif maps.upload_map(routename, file):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a map, check format (.jpg) and size (preferably < 300 kt)")

@app.route("/show/<int:id>")
def show(id):
    data = maps.get_map(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

#Review functions

@app.route("/reviewroute")
def reviewroute():
    routes = runroutes.get_route_names()
    return render_template("reviewroute.html", routes=routes)

@app.route("/createreview", methods=["GET", "POST"])
def createreview():
    routename = request.form["routename"]
    grade = request.form["grade"]
    review = request.form["review"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    elif reviews.create_review(routename, grade, review):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a new review")

@app.route("/browsereviews")
def browsereviews():
    reviewlist = reviews.get_reviews()
    return render_template("browsereviews.html", reviewlist=reviewlist)

#Time functions

@app.route("/newtime")
def newtime():
    routes = runroutes.get_route_names()
    return render_template("newtime.html", routes=routes)

@app.route("/createtime", methods=["GET", "POST"])
def createtime():
    routename = request.form["routename"]
    completion_date = request.form["completion_date"]
    completion_time = request.form["completion_time"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    elif runroutes.create_time(routename, completion_time, completion_date):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while adding a new running time")
