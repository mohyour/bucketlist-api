from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates
import jwt
import re
from datetime import datetime, timedelta

db = SQLAlchemy()
print ('importing module {}'.format(__name__))
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship(
        'BucketList', order_by='BucketList.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def valid_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @validates('email')
    def validate_email(self, key, address):
        email_regex = r'\b[\w.-]+?@\w+?\.\w+?\b'
        pattern = re.compile(email_regex)
        assert pattern.match(address)
        return address

    def generate_token(self, user_id):
        """ Generates user token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


class BucketList(db.Model):
    """Creating the bucketlist table"""

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    owner = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, owner):
        """Initialize with name and owner"""
        self.name = name
        self.owner = owner

    def save(self):
        """Save new bucketlist to db"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete entry from db"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all bucketlist entries"""
        return BucketList.query.filter_by(owner=user_id)

    def __repr__(self):
        return "BucketList {0}".format(self.name)
