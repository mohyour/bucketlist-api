from . import bucketlist_blueprint
from flask.views import MethodView
from flask import jsonify, request, make_response
from src.models import BucketList, User
from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization'].split(" ")[1]
            token_data = User.decode_token(token)
            if token_data != int(token_data):
                return jsonify({
                    "message": token_data
                })
            user_id = token_data
        except:
            return jsonify({'message': 'Please provide a valid token'})
        return f(user_id, *args, **kwargs)
    return decorated

def get_response_object(bucketlist):
    obj = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'owner_id': bucketlist.owner,
        'created_at': bucketlist.created_at,
        'updated_at': bucketlist.updated_at
    }
    return obj

def homepage():
    return jsonify({
        "message": "Welcome to bucket list API"
    }), 200


@bucketlist_blueprint.route('/lists', methods=['POST'])
@auth_required
def create_bucketlists(user_id):
    try:
        name = request.data["name"].strip()
        if name:
            bucketlist = BucketList(name=name, owner=user_id)
            bucketlist.save()
            response = get_response_object(bucketlist)
            return make_response(jsonify(response)), 201
        else:
            return make_response(jsonify({
                "message": "Bucketlist name cannot be empty"
            })), 400
    except KeyError:
        return(jsonify({
            "message": "Check payload. Bucketlist name is needed"
        }))


@bucketlist_blueprint.route('/lists', methods=['GET'])
@auth_required
def get_bucketlists(user_id):
    bucketlists = BucketList.get_all(user_id)
    all_lists = []

    for bucketlist in bucketlists:
        obj = get_response_object(bucketlist)
        all_lists.append(obj)
    response = jsonify(all_lists)
    return make_response(response), 200


@bucketlist_blueprint.route("/lists/<int:id>", methods=["GET"])
@auth_required
def get_by_id(user_id, id):
    bucket = BucketList.query.filter_by(id=id).first()
    if not bucket:
        return jsonify({
            "message": "Bucket list not found"
        }), 404
    return jsonify(get_response_object(bucket)), 200


@bucketlist_blueprint.route("/lists/<int:id>", methods=["PUT"])
@auth_required
def edit_by_id(user_id, id):
    bucket = BucketList.query.filter_by(id=id).first()
    if bucket == None:
        return jsonify({
            "message": "Bucket list not found"
        }), 404

    if bucket.owner == user_id:
            name = str(request.data.get('name', ''))
            bucket.name = name
            bucket.save()
            return jsonify(get_response_object(bucket)), 200
    else:
        return jsonify({
            "message": "You cannot edit another user's bucketlist"
        }), 401
        


@bucketlist_blueprint.route("/lists/<int:id>", methods=["DELETE"])
@auth_required
def delete_by_id(user_id, id):
    bucket = BucketList.query.filter_by(id=id).first()
    if not bucket:
        return jsonify({
            "message": "Bucket list not found"
        }), 404

    if bucket.owner == user_id:
        bucket.delete()
        return jsonify({
            "message": "Bucket list successfully deleted"
        }), 200
    else:
        return jsonify({
            "message": "You cannot delete another user's bucketlist"
        }), 401
    
