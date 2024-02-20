#!/usr/bin/env python3
''' user routes '''
from flask import jsonify, abort, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
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

    user = db.find_one(User, User.email)
    if user:
        return jsonify(409, description='Email already exists')
    
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'],
                phone=data['phone'],
                password=hashed_password)
    db.new(user)
    db.save()

    token = create_access_token(identity=user.email)

    return jsonify({
        'access_token': token,
        'user': {
            'email': user.email,
            'phone': user.phone
        }
    }), 201


@app_views.route("/login", methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' login user '''
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json() 
    if 'email' not in data:
        abort(400, description='Missing Email')
    if 'password' not in data:
        abort(400, description="Missing password")

    user = db.find_one(User, User.email == data['email'])
    if not user:
        abort(401, description="Invalid email or password")

    if not check_password_hash(user.password, data['password']):
        abort(401, description="Invalid email or password")

    user_data = {
    'email': user.email,
    'userid': user.userid,
    'phone_number': user.phone_number
    }

    token = create_access_token(identity=user_data)

    return jsonify({
        'access_token': token,
        'user': {
            'email': user.email,
            'phone': user.phone
        }
    }), 200

@app_views.route("/users", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    print(current_user)
    if not current_user:
        return jsonify(message="Unauthorized"), 401
    
    if current_user.get('role') != 'ADMIN':
        return jsonify(message="Admin privileges required"), 403

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