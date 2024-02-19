#!/usr/bin/env python3
''' user routes '''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.engine.mysqldb_config import MysqlConfig
from models.user import User

db = MysqlConfig()
db.reload()

@app_views.route('/register/', methods=['POST'], strict_slashes=False)
def register() -> str:
    ''' Register new User'''
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json() 
    if 'email' not in data:
        abort(400, description='Missing Email')
    if 'phone' not in data:
        abort(400, description="Missing Phone Number")
    if 'password' not in data:
        abort(400, description="Missing password")

    # theres something missing here 
    # make sure to come back and correct it
    user = db.find_one(User, User.email)
    if user:
        return jsonify(409, description='Email already exists')
    user = User(email=data['email'],
                phone=data['phone'],
                password=data['password'])
    db.new(user)
    db.save()
    return jsonify(201, description='User Created')

    
@app_views.route("/users", methods=['GET'], strict_slashes=False)    
def get_users():
    users = db.all(User).values()
    users_list = [user.__custom_dict__() for user in users]
    return jsonify(users_list)

@app_views.route("/users/<string:user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = db.find_one(User, User.id == user_id)
    if not user:
        abort(400, description = "User not Found")
    if not request.get_json():
        abort(400, description= "Not a JSON")
    print(user)
    data = request.get_json()

    # get to know more about getattr and setattr
    for key, value in data.items():
        if key != "id" and hasattr(user, key):
            setattr(user, key, value)
    db.save()
    return jsonify(user.__custom_dict__()), 200