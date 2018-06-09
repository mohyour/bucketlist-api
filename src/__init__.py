from flask_api import FlaskAPI
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


db = SQLAlchemy() # database initialization
app = FlaskAPI(__name__, instance_relative_config=True)

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) # connects app to db

    # register blueprints
    from src.views import bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)

    return app
    
