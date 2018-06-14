from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from src.models import db

app = FlaskAPI(__name__, instance_relative_config=True)

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) # connects app to db

    # register bucketlist
    from src.bucketlist import bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)

    # register user blueprint
    from src.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
    