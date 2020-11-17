from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)




from resources.user import User

class TokenResource(Resource):
    def post(self):

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.get_by_email(email=email)

        if not user:
            return {'message': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.id)
        refresh_token = create_access_token(identity=user.id)


        return {'access token': access_token}, HTTPStatus.OK







