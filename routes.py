from flask import redirect, render_template, request, session
from app import app
import users
import runroutes
import reviews
from db import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
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

@app.route("/create", methods=["GET", "POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    length = request.form["length"]
    coordinates = request.form["coordinates"]
    if runroutes.create(name, type, length, coordinates):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a new route")

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

@app.route("/browseroutes")
def browseroutes():
    routes = runroutes.get_routes()
    return render_template("browseroutes.html", routes=routes)

@app.route("/newroute")
def newroute():
    return render_template("newroute.html")

@app.route("/savemain")
def savemain():
    return render_template("savemain.html")


@app.route("/newmap")
def newmap():
    routes = runroutes.get_route_names()
    return render_template("newmap.html", routes=routes)

@app.route("/uploadmap", methods=["GET", "POST"])
def uploadmap():
    routename = request.form["routename"]
    file = request.files["file"]
    filename = file.filename
    if not filename.endswith(".jpg"):
        return render_template(error.html, message="Error, invalid format, use .jpg images")
    data = file.read()
    if len(data) > 300*1024:
        return render_template(error.html, message="Error, file is too big, size limit is 300 kt")
    route_id = runroutes.get_route_id(routename)
    sql = "INSERT INTO maps (filename, route_id, data) VALUES (:filename, :route_id, :data)"
    db.session.execute(sql, {"filename":filename, "route_id":route_id, "data":data})
    db.session.commit()
    return redirect("/")

@app.route("/reviewroute")
def reviewroute():
    routes = runroutes.get_route_names()
    return render_template("reviewroute.html", routes=routes)

@app.route("/createreview", methods=["GET", "POST"])
def createreview():
    routename = request.form["routename"]
    grade = request.form["grade"]
    review = request.form["review"]
    if reviews.create_review(routename, grade, review):
        return redirect("/")
    else:
        return render_template("error.html", message="Error while creating a new review")

@app.route("/browsereviews")
def browsereviews():
    reviewlist = reviews.get_reviews()
    return render_template("browsereviews.html", reviewlist=reviewlist)
