#!/usr/bin/env python3
''' index views '''
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/status/', methods=['GET'], strict_slashes=False)
def status() -> str:
    ''' return current status '''
    return jsonify({"status": "OK"})