#!/usr/bin/env python3
''' user routes '''
from flask import jsonify, abort, request
from api.v1.views import app_views

@app_views.route('/register/', methods=['POST'], strict_slashes=False)
def register() -> str:
    ''' Register new User'''
    data = request.get_json
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description='Missing Email')
    if 'phone' not in data:
        abort(400, description="Missing Phone Number")
    if 'password' not in data:
        abort(400, description="Missing password")    

