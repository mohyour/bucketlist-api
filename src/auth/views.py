from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from src.models import User


class Signup(MethodView):
    """Registers new user."""
    def post(self):
        print(request.data['username'])
        email = request.data['email']
        password = request.data['password']
        username = request.data['username']

        user = User.query.filter_by(email=email).first()

        if not user:
            try:
                user = User(username=username, email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202

signup_view = Signup.as_view('register_view')
auth_blueprint.add_url_rule(
    '/auth/signup',
    view_func=signup_view,
    methods=['POST'])
