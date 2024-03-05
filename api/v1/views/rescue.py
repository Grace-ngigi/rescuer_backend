#!/usr/bin/env python3
''' Rescues '''

from models.rescue import Rescue
from api.v1.views import app_views
from models.rescue import RescueStatus
from models.engine.mysqldb_config import MysqlConfig 
from datetime import datetime
from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

db = MysqlConfig()
db.reload()


@app_views.route("/rescues", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_rescue():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, "Unauthorized")

    ''' create a rescue '''
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json() 
    if 'species' not in data:
        abort(400, description='Missing Species')
    if 'age' not in data:
        abort(400, description='Missing Age')
    if 'description' not in data:
        abort(400, description='Missing description') 
    if 'image_url' not in data:
        abort(400, description='Missing image_url')
    if 'location' not in data:
        abort(400, description='Missing location')

    rescue = Rescue(
        species=data['species'],
        age=data['age'],
        description=data['description'],
        image_url=data['image_url'],
        user_id=current_user['id'],
        location=data['location'],
        status = RescueStatus.RESCUED.value
        )
    rescue.created_at = datetime.utcnow()
    rescue.created_by = current_user['id']

    db.new(rescue)
    db.save()

    return jsonify(rescue.__custom_dict__()), 201

@app_views.route("/rescue/<string:rescue_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_rescue(rescue_id):
    ''' retrieve rescue '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    rescue = db.find_one(Rescue, Rescue.user_id == current_user['id'] and Rescue.id == rescue_id )
    if not rescue:
        abort(404, decription="Rescue Not Found")

    return jsonify(rescue.__custom_dict__()), 200


@app_views.route("/user/rescues", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user_rescues():
    ''' find all rescues '''
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    rescues = db.find_many(Rescue, Rescue.user_id == current_user['id'])
    rescues_list = [rescue.__custom_dict__()  for rescue in rescues]
    return jsonify(rescues_list), 200


@app_views.route("/ready/rescues", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_ready_rescues():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")
        
    rescues = db.find_many(Rescue, Rescue.status == RescueStatus.READY.value)
    rescues_list = [rescue.__custom_dict__()  for rescue in rescues]
    return jsonify(rescues_list), 200


@app_views.route("/rescues", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_rescues():
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")
    
    if current_user.get('role') != 'ADMIN':
        abort(403, description="Admin privileges required")

    rescues = db.all(Rescue).values()
    rescues_list = [rescue.__custom_dict__() for rescue in rescues]
    return jsonify(rescues_list), 200


@app_views.route("/rescue/<string:rescue_id>", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_rescue(rescue_id):
    current_user = get_jwt_identity()
    if not current_user:
        abort(401, description="Unauthorized")

    if current_user.get('role') != 'ADMIN':
        abort(403, description="Admin privileges required")
    
    rescue = db.find_one(Rescue, Rescue.id == rescue_id)
    if not rescue:
        abort(400, description = "rescue not Found")
    if not request.get_json():
        abort(400, description= "Not a JSON")
    data = request.get_json()

    for k,v in data.items():
        if k not in ["id", "created_at", "created_by","updated_at", "updated_by"] and hasattr(rescue, k):
            setattr(rescue, k, v)
    rescue.updated_at = datetime.utcnow()
    rescue.updated_by = current_user['id']

    db.save()
    return jsonify(rescue.__custom_dict__()), 200
