#!/usr/bin/env python3
''' entry point '''
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from api.v1.views import app_views


from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'awesomeamazement'
jwt = JWTManager(app)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

if __name__ == '__main__':
    host = "0.0.0.0"
    port = "5100"
    app.run(host, port)
