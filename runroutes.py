from sqlalchemy import update
from db import db
import users

#Create and hide functions

def create_route(name, type, length, coordinates):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO routes (name, type, length, coordinates, created_at, created_by) VALUES (:name, :type, :length, :coordinates, NOW(), :created_by)"
    db.session.execute(sql, {"name":name, "type":type, "length":length, "coordinates":coordinates, "created_by":user_id})
    db.session.commit()
    return True

def create_time(routename, completion_time, completion_date):
    runner_id = users.get_user_id()
    route_id = get_route_id(routename)
    if runner_id == 0:
        return False
    sql = "INSERT INTO times (route_id, runner_id, completion_date, completion_time, created_at) VALUES (:route_id, :runner_id, :completion_date, :completion_time, NOW())"
    db.session.execute(sql, {"route_id":route_id, "runner_id":runner_id, "completion_date":completion_date, "completion_time":completion_time})
    db.session.commit()
    return True

#Get functions

def get_routes():
    sql = "SELECT R.name, R.type, R.coordinates, R.length, U.username, R.id FROM routes R, users U WHERE U.id = R.created_by"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_names():
    sql = "SELECT NAME from routes"
    result = db.session.execute(sql)
    return result.fetchall()

def get_route_name(route_id):
    sql = "SELECT name FROM routes WHERE id=:route_id"
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
    sql = "SELECT R.name, T.completion_date, T.completion_time FROM times T, routes R WHERE T.route_id = R.id AND T.runner_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_routes_by_user(id):
    sql = "SELECT * FROM routes where created_by=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()
