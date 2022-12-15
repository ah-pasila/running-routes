from db import db
import users
from flask import make_response

def create(name, type, length, coordinates):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO routes (name, type, length, coordinates, created_at, created_by) VALUES (:name, :type, :length, :coordinates, NOW(), :created_by)"
    db.session.execute(sql, {"name":name, "type":type, "length":length, "coordinates":coordinates, "created_by":user_id})
    db.session.commit()
    return True

def get_routes():
    sql = "SELECT R.name, R.type, R.coordinates, R.length, U.username, R.id FROM routes R, users U WHERE U.id = R.created_by"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_names():
    sql = "SELECT name from routes"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_id(routename):
    sql = "SELECT id FROM routes WHERE name=:routename"
    result = db.session.execute(sql, {"routename":routename})
    route_info = result.fetchone()
    route_id = route_info[0]
    return route_id

#def savemap():
#    routename = request.form[routename]
#    file = request.files["file"]
#    file = file.filename
#    if not name.endswith(".jpg"):
#        return "Invalid filename"
#    data = file.read()
#    if len(data) > 300*1024:
#        return "Too big file"
#    route_id = get_route_id(routename)
#    sql = "INSERT INTO maps (name,data,route_id) VALUES (:name,:data,:route_id)"
#    db.session.execute(sql, {"name":name, "data":data, "route_id":route_id })
#    db.session.commit()
#    return "OK"
