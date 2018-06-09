from flask_api import FlaskAPI
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


db = SQLAlchemy() # database initialization
app = FlaskAPI(__name__, instance_relative_config=True)

def create_app(config_name):
    from src.models import BucketList
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) # connects app to db
    

    @app.route('/lists/', methods=['POST', 'GET'])
    def create_bucketlists():
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = BucketList(name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'created_at': bucketlist.created_at,
                    'updated_at': bucketlist.updated_at
                })
                response.status_code = 201
                return response
            
            else:
                return jsonify({
                    "message": "enter bucketlist name"
                })

        else:
            bucketlists = BucketList.get_all()
            all_lists = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'created_at': bucketlist.created_at,
                    'updated_at': bucketlist.updated_at
                }
                all_lists.append(obj)
            response = jsonify(all_lists)
            response.status_code = 200
            return response
            
    return app
