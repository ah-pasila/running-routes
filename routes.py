from flask import redirect, render_template, request, session, make_response
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
    sql = "INSERT INTO maps (filename, route_id, data, visibility, created_at) VALUES (:filename, :route_id, :data, TRUE, NOW())"
    db.session.execute(sql, {"filename":filename, "route_id":route_id, "data":data})
    db.session.commit()
    return redirect("/")

def hide_map(id):
    sql = "UPDATE maps SET visibility=FALSE WHERE maps.route_id=id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

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

@app.route("/show/<int:id>")
def show(id):
    sql = "SELECT data FROM maps M, routes R WHERE M.route_id=:id AND R.visibility=TRUE"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/newtime")
def newtime():
    routes = runroutes.get_route_names()
    return render_template("newtime.html", routes=routes)

@app.route("/browsepersonal", methods=["GET", "POST"])
def browsepersonal():
    id = users.get_user_id()
    times = runroutes.get_route_times_by_user(id)
    routes = runroutes.get_routes_by_user(id)
    reviewlist = reviews.get_reviews_by_user(id)
    return render_template("browsepersonal.html", times=times, routes=routes, reviewlist=reviewlist)

@app.route("/deleteroute", methods=["GET", "POST"])
def deleteroute():
    routename=request.form["routename"]
    route_id=runroutes.get_route_id(routename)
    runroutes.hide_route(id)
    return redirect("/")

@app.route("/createtime", methods=["GET", "POST"])
def createtime():
    routename = request.form["routename"]
    completion_date = request.form["completion_date"]
    completion_time = request.form["completion_time"]
    if runroutes.createtime(routename, completion_time, completion_date):
       return redirect("/")
    else:
       return render_template("error.html", message="Error while adding a new running time")
