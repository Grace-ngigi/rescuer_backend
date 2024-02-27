#!/usr/bin/env python3
''' user routes '''
from flask import jsonify, abort, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from api.v1.views import app_views
from models.engine.mysqldb_config import MysqlConfig
from models.user import User
from datetime import datetime



db = MysqlConfig()
db.reload()

@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register() -> str:
    ''' Register new User'''
    # if not request.get_json():
    #     abort(400, description="Not a JSON")
    data = request.get_json() 
    if 'email' not in data:
        abort(400, description='Missing Email')
    if 'phone' not in data:
        abort(400, description="Missing Phone Number")
    if 'password' not in data:
        abort(400, description="Missing password")

    existing_user = db.find_one(User, User.email== data['email'])
    print(existing_user)
    if existing_user:
        return abort(400, description='Email already exists')
    
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'],
                phone=data['phone'],
                password=hashed_password)
    print(datetime.utcnow())
    user.created_at = datetime.utcnow()
    user.created_by = user.id
    db.new(user)
    db.save()

    user_data = {
    'email': user.email,
    'id': user.id,
    'phone': user.phone,
    'role': user.role
    }

    token = create_access_token(identity=user_data)

    return jsonify({
        'access_token': token,
        'user': {
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at,
            'created_by': user.created_by
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
    'id': user.id,
    'phone': user.phone,
    'role': user.role
    }

    token = create_access_token(identity=user_data)

    return jsonify({
        'access_token': token,
        'user': {
            'email': user.email,
            'phone': user.phone,
            'role':user.role
        }
    }), 200

@app_views.route("/users", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")
    
    if current_user.get('role') != 'ADMIN':
        abort(403, description="Admin privileges required")

    users = db.all(User).values()
    users_list = [user.__custom_dict__() for user in users]
    return jsonify(users_list),200

@app_views.route("/profile", methods=['GET'], strict_slashes=False)
@jwt_required()
def retrieve_profile():
    ''' get profile '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    user = db.find_one(User, User.id == current_user['id'])
    if not user:
        abort(404, description="User Not Found")

    print("Retrieved User:", user.__dict__)
    return jsonify(user.__custom_dict__()), 200

@app_views.route("/profile", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")
    
    user = db.find_one(User, User.id == current_user['id'])
    if not user:
        abort(400, description = "User not Found")
    if not request.get_json():
        abort(400, description= "Not a JSON")
    data = request.get_json()

    # get to know more about getattr and setattr
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "updated_by"] and hasattr(user, key):
            setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    user.updated_by = current_user['id']

    db.save()
    return jsonify(user.__custom_dict__()), 200

# @app_views.route("/profile", methods=['DELETE'], strict_slashes=False)
# @jwt_required()
# def delete_profile():
#     ''' deleting user profile '''
#     current_user = get_jwt_identity()

#     if not current_user:
#         abort(401, description="Unauthorized")

#     user = db.find_one(User, current_user.id)
#     if not user:
#         abort(404, description="User Not Found")

    # write code to delete the user
    # You know, updating the isdeleted flag

