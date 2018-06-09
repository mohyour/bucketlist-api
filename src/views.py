from models import BucketList
from scr import app
from flask import abort, jsonify, request

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
        