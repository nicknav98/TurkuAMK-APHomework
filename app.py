from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from resources.instruction import InstructionListResource, InstructionResource, InstructionPublishResource
from extensions import jwt
from resources.user import UserResource, MeResource
from resources.token import TokenResource



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app
def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
def register_resources(app):
    api = Api(app)
    api.add_resource(InstructionListResource, '/instructions')
    api.add_resource(InstructionResource, '/instructions/<int:instruction_id>')
    api.add_resource(InstructionPublishResource, '/instructions/<int:instruction_id>/ publish')
def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

def register_resources(app):
    api = Api(app)


    api.add_resource(UserResource, '/users/<string:username>')

    api.add_resource(TokenResource, '/token')

api.add_resource(MeResource, '/me')


if __name__ =='__main__':
    app = create_app()
    app.run()
