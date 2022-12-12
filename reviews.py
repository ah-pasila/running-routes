from db import db
import users, routes, runroutes

def create_review(routename, grade, review):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    route_id = runroutes.get_route_id(routename)
    sql = "INSERT INTO reviews (grade, route_id, review, created_by) VALUES (:grade, :route_id, :review, :created_by)"
    db.session.execute(sql, {"grade":grade, "route_id":route_id, "review":review, "created_by":user_id})
    db.session.commit()
    return True

def get_reviews():
    sql = "SELECT RO.name, U.username, RE.grade, RE.review FROM reviews RE, routes RO, users U WHERE U.id = RE.created_by AND RE.route_id = RO.id"
    reviews = db.session.execute(sql)
    return reviews.fetchall()
