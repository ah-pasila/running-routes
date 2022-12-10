from db import db
import users

def create(name, type, length):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO routes (name, type, length, created_at, created_by) VALUES (:name, :type, :length, NOW(), :created_by)"
    db.session.execute(sql, {"name":name, "type":type, "length":length, "created_by":"1"})
    db.session.commit()
    return True

def get_routes():
    sql = "SELECT R.name, R.type, R.length, U.username FROM routes R, users U WHERE U.id = R.created_by"
    result = db.session.execute(sql)
    return result.fetchall()

def savemap():
    file = request.files["file"]
    name = file.filename
    if not name.endswith(".jpg"):
        return "Invalid filename"
    data = file.read()
    if len(data) > 300*1024:
        return "Too big file"
    sql = "INSERT INTO maps (name,data) VALUES (:name,:data)"
    db.session.execute(sql, {"name":name, "data":data})
    db.session.commit()
    return "OK"

#@app.route("/show/<int:id>")
#def showmap(id):
#    sql = "SELECT data FROM maps WHERE id=:id"
#    result = db.session.execute(sql, {"id":id})
#    data = result.fetchone()[0]
#    response = make_response(bytes(data))
#    response.headers.set("Content-Type", "image/jpeg")
#    return response
