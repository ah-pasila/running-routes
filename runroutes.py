from db import db
import users

def create(name, type, length):
    username = users.username_check()
    if username == 0:
        return False
    sql = "INSERT INTO routes (name, type, length, created_at) VALUES (:name, :type, :length, NOW())"
    db.session.execute(sql, {"name":name, "type":type, "length":length})
    db.session.commit()
    return True

def browseroutes():
    sql = "SELECT id, name, type, length FROM routes"
    result = db.session.execute(sql)
    routes = result.fetchall()
    db.session.commit()
