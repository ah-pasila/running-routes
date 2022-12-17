from db import db
import users, routes, runroutes

def create_review(routename, grade, review):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    route_id = runroutes.get_route_id(routename)
    sql = "INSERT INTO reviews (grade, route_id, review, created_by, visibility, created_at) VALUES (:grade, :route_id, :review, :created_by, TRUE, NOW())"
    db.session.execute(sql, {"grade":grade, "route_id":route_id, "review":review, "created_by":user_id})
    db.session.commit()
    return True

def hide_review(id):
    sql = "UPDATE reviews SET visibility=FALSE WHERE route_id=id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_reviews():
    sql = "SELECT RO.name, U.username, RE.grade, RE.review FROM reviews RE, routes RO, users U WHERE U.id = RE.created_by AND RE.route_id = RO.id AND RO.visibility=TRUE"
    reviews = db.session.execute(sql)
    return reviews.fetchall()

def get_reviews_by_user(id):
    sql = "SELECT RO.name, RE.grade, RE.review FROM routes RO, reviews RE, users U where RE.route_id=RO.id AND RE.created_by=U.id AND RO.visibility=TRUE"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()
