from . import bucketlist_blueprint
from flask.views import MethodView
from flask import jsonify, request
from src.models import BucketList, User
from functools import wraps


def auth_required(f):
    """Checks user authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization'].split(" ")[1]
            token_data = User.decode_token(token)
            if not isinstance(token_data, int):
                response = {
                    "message": token_data
                }
                return jsonify(response), 401
            user_id = token_data
        except:
            response = {
                'message': 'Please provide a valid token'
            }
            return jsonify(response), 401
        return f(user_id, *args, **kwargs)
    return decorated


def get_response_object(bucketlist):
    """Custom response for user bucket details"""
    obj = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'owner_id': bucketlist.owner,
        'created_at': bucketlist.created_at,
        'updated_at': bucketlist.updated_at
    }
    return obj


@bucketlist_blueprint.route('/', methods=['GET'])
def homepage():
    """Homepage message"""
    response = {
        "message": "Welcome to bucket list API"
    }
    return jsonify(response), 200


@bucketlist_blueprint.route('/lists', methods=['POST'])
@auth_required
def create_bucketlists(user_id):
    """Create bucket list"""

    try:
        name = request.data["name"].strip()
        if name:
            bucketlist = BucketList(name=name, owner=user_id)
            bucketlist.save()
            response = get_response_object(bucketlist)
            return jsonify(response), 201
        else:
            return jsonify({
                "message": "Bucketlist name cannot be empty"
            }), 400
    except KeyError:
        response = {
            "message": "Check payload. Bucketlist name is needed"
        }
        return jsonify(response), 400


@bucketlist_blueprint.route('/lists', methods=['GET'])
@auth_required
def get_bucketlists(user_id):
    """Get all bucket list for the authenticated user"""

    bucketlists = BucketList.get_all(user_id)
    all_lists = []

    for bucketlist in bucketlists:
        obj = get_response_object(bucketlist)
        all_lists.append(obj)
    response = all_lists
    return jsonify(response), 200


@bucketlist_blueprint.route("/lists/<int:id>", methods=["GET"])
@auth_required
def get_by_id(user_id, id):
    """Get bucket list by id"""

    bucket = BucketList.query.filter_by(id=id).first()
    if not bucket:
        response = {
            "message": "Bucket list not found"
        }
        return jsonify(response), 404
    response = get_response_object(bucket)
    return jsonify(response), 200


@bucketlist_blueprint.route("/lists/<int:id>", methods=["PUT"])
@auth_required
def edit_by_id(user_id, id):
    """Edit bucket list by id"""

    bucket = BucketList.query.filter_by(id=id).first()
    if bucket == None:
        response = {
            "message": "Bucket list not found"
        }
        return jsonify(response), 404

    if bucket.owner == user_id:
        name = str(request.data.get('name', ''))
        bucket.name = name
        bucket.save()
        response = get_response_object(bucket)
        return jsonify(response), 200
    else:
        response = {
            "message": "You cannot edit another user's bucketlist"
        }
        return jsonify(response), 401


@bucketlist_blueprint.route("/lists/<int:id>", methods=["DELETE"])
@auth_required
def delete_by_id(user_id, id):
    """Delete bucket list by id"""

    bucket = BucketList.query.filter_by(id=id).first()
    if not bucket:
        response = {
            "message": "Bucket list not found"
        }
        return jsonify(response), 404

    if bucket.owner == user_id:
        bucket.delete()
        response = {
            "message": "Bucket list successfully deleted"
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "You cannot delete another user's bucketlist"
        }
        return jsonify(response), 401
