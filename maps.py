from db import db
from flask import Flask, redirect, render_template, request, session, make_response
import runroutes

#Create functions

def upload_map(routename, file):
    route_id = runroutes.get_route_id(routename)
    data = file.read()
    filename = file.filename
    sql = "INSERT INTO maps (filename, route_id, data, created_at) VALUES (:filename, :route_id, :data, NOW())"
    db.session.execute(sql, {"filename":filename, "route_id":route_id, "data":data})
    db.session.commit()
    return True

#Get functions

def get_map(route_id):
    sql = "SELECT M.data FROM maps M, routes R WHERE M.route_id=:route_id and M.route_id=R.id"
    result = db.session.execute(sql, {"route_id":route_id})
    data = result.fetchone()[0]
    return data
