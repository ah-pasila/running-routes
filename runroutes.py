from db import db
import users
from flask import make_response
import reviews
import routes

def create(name, type, length, coordinates):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO routes (name, type, length, coordinates, created_at, created_by, visibility) VALUES (:name, :type, :length, :coordinates, NOW(), :created_by, TRUE)"
    db.session.execute(sql, {"name":name, "type":type, "length":length, "coordinates":coordinates, "created_by":user_id})
    db.session.commit()
    return True

def createtime(routename, completion_time, completion_date):
    runner_id = users.get_user_id()
    route_id = get_route_id(routename)
    if runner_id == 0:
        return False
    sql = "INSERT INTO times (route_id, runner_id, completion_date, completion_time, visibility, created_at) VALUES (:route_id, :runner_id, :completion_date, :completion_time, TRUE, NOW())"
    db.session.execute(sql, {"route_id":route_id, "runner_id":runner_id, "completion_date":completion_date, "completion_time":completion_time})
    db.session.commit()
    return True

def hide_route(id):
    sql = "UPDATE routes SET visibility=FALSE WHERE routes.id=id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    hide_time(id)
    reviews.hide_review(id)
    routes.hide_map(id)

def hide_time(id):
    sql = "UPDATE times SET visibility=FALSE WHERE times.route_id=id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()

def get_routes():
    sql = "SELECT R.name, R.type, R.coordinates, R.length, U.username, R.id FROM routes R, users U WHERE U.id = R.created_by AND R.visibility=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_names():
    sql = "SELECT NAME from routes WHERE visibility=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_name(route_id):
    sql = "SELECT name FROM routes WHERE id=route_id AND visibility=TRUE"
    result = db.session.execute(sql, {"route_id":route_id})
    route.info = result.fetchone()
    routename = route_info[1]
    return routename

def get_route_id(routename):
    sql = "SELECT id FROM routes WHERE name=:routename"
    result = db.session.execute(sql, {"routename":routename})
    route_info = result.fetchone()
    route_id = route_info[0]
    return route_id

def get_route_times_by_user(id):
    sql = "SELECT R.name, T.completion_date, T.completion_time FROM times T, routes R WHERE T.route_id = R.id AND T.runner_id=:id AND R.visibility=TRUE"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_routes_by_user(id):
    sql = "SELECT * FROM routes where created_by=:id AND routes.visibility=TRUE"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

