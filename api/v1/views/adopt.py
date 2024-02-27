#!/usr/bin/env python3
''' adopts '''
from models.adopt import Adopt
from models.rescue import Rescue, RescueStatus
from api.v1.views import app_views
from models.adopt import AdoptStatus
from models.engine.mysqldb_config import MysqlConfig 
from datetime import datetime
from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

db = MysqlConfig()
db.reload()

@app_views.route("/adopt", methods=['POST'], strict_slashes=False)
@jwt_required()
def adopt():
    ''' create a request '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description = "Unauthorized")

    if 'rescue_id' not in request.args:
        abort(400, description = 'Missing Request Id')

    rescue_id = request.args.get('rescue_id')

    adopt = Adopt(
        user_id=current_user['id'],
        rescue_id=rescue_id,
        status=AdoptStatus.INIT.value
    )
    adopt.created_at = datetime.utcnow()
    adopt.created_by = current_user['id']
    try:
        db.new(adopt)
    except Exception as e:
        db.rollback()
        abort(500, decription = f"Failed to create adoption: {str(e)}")

    rescue = db.find_one(Rescue, Rescue.id == rescue_id)
    if rescue:
        rescue.status = RescueStatus.ADOPTED.value
        db.save()
    else:
        abort(404, description="Rescue not found")
        
    return jsonify(adopt.__custom_dict__()), 201

@app_views.route("/adopt/<string:adopt_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_adopt(adopt_id):
    ''' retrieve adopt '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    adopt = db.find_one(Adopt, Adopt.user_id == current_user['id'] and Adopt.id == adopt_id)
    if not adopt:
        abort(404, decription="Adopt Not Found")

    return jsonify(adopt.__custom_dict__()), 200

@app_views.route("user/adopts", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user_adopts():
    ''' find all adopts '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    adopts = db.find_many(Adopt, Adopt.user_id == current_user['id'])
    adopts_list = [adopt.__custom_dict__()  for adopt in adopts]
    return jsonify(adopts_list), 200


@app_views.route("/adopts", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_adopts():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")
    
    if current_user.get('role') != 'ADMIN':
        abort(403, description="Admin privileges required")

    adopts = db.all(Adopt).values()
    adopts_list = [adopt.__custom_dict__() for adopt in adopts]
    return jsonify(adopts_list), 200

@app_views.route("/adopt/<string:adopt_id>", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_adopt(adopt_id):
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    if current_user.get('role') != 'ADMIN':
        abort(403, description="Admin privileges required")
    
    adopt = db.find_one(Adopt, Adopt.id == adopt_id)
    if not adopt:
        abort(400, description = "adopt not Found")
    if not request.get_json():
        abort(400, description= "Not a JSON")
    data = request.get_json()

    for k,v in data.items():
        if k not in ["id", "created_at", "created_by","updated_at", "updated_by"] and hasattr(adopt, k):
            setattr(adopt, k, v)
    adopt.updated_at = datetime.utcnow()
    adopt.updated_by = current_user['id']

    db.save()
    return jsonify(adopt.__custom_dict__()), 200