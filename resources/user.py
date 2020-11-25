from flask import request

from extensions import db
from flask_jwt_extended import jwt_optional, get_jwt_identity
from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))


class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email

        }

        return data, HTTPStatus.OK




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    recipes = db.relationship('Instructions', backref='user')


@classmethod
def get_by_id(cls,id):

    return cls.query.filter_by(id=id).first()


def get_by_username(cls, username):
    return cls.query.filter_by(username=username).first() @ classmethod


def get_by_email(cls, email):
    return cls.query.filter_by(email=email).first()


def save(self):
    db.session.add(self)
    db.session.commit()


class UserResource(Resource):
    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }

        else:
            data = {
                'id': user.id,
                'username': user.username
            }

        return data, HTTPStatus.OK



class UserListResource:
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return{'message':'Validation erros', 'errors': errors},HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already exists'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already exists'}, HTTPStatus.BAD_REQUEST


        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED



