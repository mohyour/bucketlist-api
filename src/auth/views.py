from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from src.models import User
import sqlalchemy


class Signup(MethodView):
    """Registers new user."""
    def post(self):
        try:
            email = request.data['email']
            password = request.data['password']
            username = request.data['username']
            if not username:
                return jsonify({
                    'message': 'username cannot be empty'
                })
        except KeyError:
            return jsonify({
                "message": "Check payload. username, email and password are needed"
            })

        user = User.query.filter_by(email=email).first()

        if not user:
            try:
                user = User(username=username, email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully.'
                }
                return jsonify(response), 201
            except AssertionError as e:
                response = {
                    'message': "Invalid email"
                }
                return jsonify(response), 401
            except sqlalchemy.exc.IntegrityError as e:
                    return({
                        "message": "Username already exist"
                    }), 400
        else:
            response = {
                'message': 'User already exists.'
            }

            return jsonify(response), 409


class Signin(MethodView):
    """Sign in user"""
    def post(self):
        try:
            email = request.data['email']
            password = request.data["password"]
        except KeyError:
            return jsonify({
                "message": "Check payload. username, email and password are needed"
            })
        try:
            user = user = User.query.filter_by(email=request.data['email']).first()
            if user and user.is_valid_password(password=password):
                user_token = user.generate_token(user_id=user.id)
                response = {
                    "message": "You are now logged in",
                    "token": user_token.decode()
                }
                return jsonify(response), 201
            else:
                response = {
                    "message": "Incorrect login details"
                }
                return jsonify(response), 401

        except Exception as e:
            response = {
                "message": str(e)
            }
            return jsonify(response), 500


signup_view = Signup.as_view('signup_view')
signin_view = Signin.as_view('signin_view')

auth_blueprint.add_url_rule('/auth/signup', view_func=signup_view,
                            methods=['POST'])

auth_blueprint.add_url_rule('/auth/signin', view_func=signin_view,
                            methods=['POST'])
