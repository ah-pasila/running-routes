from db import db
from flask import redirect, render_template, request, session, make_response
import runroutes

#Create functions

def upload_map(routename, file, filename):
    route_id = runroutes.get_route_id(routename)
    data = file.read()
    route_id = runroutes.get_route_id(routename)
    sql = "INSERT INTO maps (filename, route_id, data, created_at) VALUES (:filename, :route_id, :data, NOW())"
    db.session.execute(sql, {"filename":filename, "route_id":route_id, "data":data})
    db.session.commit()
    return True

#Get functions

def get_map(id):
    sql = "SELECT data FROM maps WHERE id=id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    return response
