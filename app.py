#!/usr/bin/env python3
''' entry point '''
import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from api.v1.views import app_views


from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'awesomeamazement'
# Token expires in 24 hours
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60

jwt = JWTManager(app)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': "Method Not Allowed", 'message': error.message}), 405)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not Found", 'message': error.description}), 404)

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': "Forbidden", 'message': error.description}), 403)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': "Unauthorized", 'message': error.description}), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': "Bad Request", 'message': error.description}), 400)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': "Internal Server Error", 'message': error.description}), 500)
app.register_blueprint(app_views)

if __name__ == '__main__':
    host = "0.0.0.0"
    port = "5100"
    app.run(host, port)
