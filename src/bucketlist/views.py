from . import bucketlist_blueprint
from flask import jsonify, request, make_response
from src.models import BucketList, User


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
    try:
        authorization = request.headers['Authorization']
        try:
            user_token = authorization.split(" ")[1]
        except Exception as e:
            return jsonify({
                "message": "Check your token format"
            }), 400
        if user_token:
            user_id = User.decode_token(user_token)
            if not isinstance(user_id, str):
                if request.method == 'POST':
                    name = request.data["name"]
                    if name:
                        bucketlist = BucketList(name=name, owner=user_id)
                        bucketlist.save()
                        response = get_response_object(bucketlist)
                        return make_response(jsonify(response)), 201
                    else:
                        return make_response(jsonify({
                            "message": "enter bucketlist name"
                        })), 400

                else:
                    bucketlists = BucketList.get_all(user_id)
                    all_lists = []

                    for bucketlist in bucketlists:
                        obj = get_response_object(bucketlist)
                        all_lists.append(obj)
                    response = jsonify(all_lists)
                    return make_response(response), 200
            else:
                return make_response(jsonify({
                    "messgae": user_id
                })), 400
    except KeyError as e:
        return make_response(jsonify({
            "message": "You need to be authorised"
        })), 401

@bucketlist_blueprint.route("/lists/<int:id>", methods=["GET", "PUT", "DELETE"])
def rud_bucketlist_by_id(id, **kwargs):
    try:
        authorization = request.headers['Authorization']
        try:
            user_token = authorization.split(" ")[1]
        except Exception as e:
            return jsonify({
                "message": "Check your token format"
            })
        if user_token:
            user_id = User.decode_token(user_token)
        if not isinstance(user_id, str):
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
        else:
                return make_response(jsonify({
                    "messgae": user_id
                }))

    except KeyError as e:
        return make_response(jsonify({
            "message": "You need to be authorised"
        })), 401
