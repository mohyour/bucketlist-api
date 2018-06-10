import sys
sys.path.append("src")
from models import BucketList
from flask import Blueprint, jsonify, request

bucketlist_blueprint = Blueprint('bucketlist', __name__)


def get_response_object(bucketlist):
    obj = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'created_at': bucketlist.created_at,
        'updated_at': bucketlist.updated_at
    }
    return obj


@bucketlist_blueprint.route('/', methods=['GET'])
def homepage():
    return jsonify({
        "message": "Welcome to bucket list API"
    }), 200


@bucketlist_blueprint.route('/lists/', methods=['POST', 'GET'])
def create_get_bucketlists():
    if request.method == 'POST':
        name = str(request.data.get('name', ''))
        if name:
            bucketlist = BucketList(name)
            bucketlist.save()
            response = get_response_object(bucketlist)
            return jsonify(response), 201
        else:
            return jsonify({
                "message": "enter bucketlist name"
            }), 400

    else:
        bucketlists = BucketList.get_all()
        all_lists = []

        for bucketlist in bucketlists:
            obj = get_response_object(bucketlist)
            all_lists.append(obj)
        response = jsonify(all_lists)
        return response, 200


@bucketlist_blueprint.route("/lists/<int:id>", methods=["GET", "PUT", "DELETE"])
def rud_bucketlist_by_id(id, **kwargs):
    bucket = BucketList.query.filter_by(id=id).first()
    if not bucket:
        return jsonify({
            "message": "Bucket list not found"
        }), 404
    
    if request.method == "GET":
        return jsonify(get_response_object(bucket)), 200
        
    if request.method == "DELETE":
        bucket.delete()
        return jsonify({
            "message": "Bucket list successfully deleted"
        }), 200

    if request.method == "PUT":
        name = str(request.data.get('name', ''))
        bucket.name = name
        bucket.save()
        return jsonify(get_response_object(bucket)), 200
