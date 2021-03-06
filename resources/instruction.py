from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from http import HTTPStatus

from models.instructions import Instruction, instruction_list
from schemas.InstructionSchema import InstructionSchema

instruction_schema = InstructionSchema()
instruction_list_schema = InstructionSchema(many=True)


class InstructionListResource(Resource):

    def get(self):
        instructions = Instruction.get_all_published()

        return instruction_list_schema.dump(instructions).data, HTTPStatus.OK
    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = instruction_schema.load(data=json_data)
        if errors:
            return {'message': "Validation errors", 'errors': errors},
            HTTPStatus.BAD_REQUEST

        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()
        return instruction_schema(instruction).data, HTTPStatus.CREATED

    @jwt_required
    def patch(self, instruction_id):

        json_data = request.get_json()

        data, errors = instruction_schema.load(data=json_data, partial=('name',))


        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'instructions not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.name = data.get('name') or instruction.name
        instruction.description = data.get('description') or instruction.description
        instruction.steps = data.get('steps') or instruction.num_of_servings
        instruction.tools = data.get('tools') or instruction.cook_time
        instruction.cost = data.get('cost') or instruction.cost
        instruction.duration = data.get('duation') or instruction.duration

        instruction.save()

        return instruction_schema.dump(instruction).data, HTTPStatus.OK



class InstructionResource(Resource):

    def get(self, instruction_id):
        instructions = next((Instruction for instructions in instruction_list
                             if Instruction.id == instruction_id and Instruction.is_publish == True), None)

        if instructions is None:
            return {'message': 'instructions not found'}, HTTPStatus.NOT_FOUND

        return Instruction.data, HTTPStatus.OK





class InstructionPublishResource(Resource):

    def put(self, instruction_id):
        instructions = next((Instruction for instructions in instruction_list if Instruction.id == instruction_id), None)

        if Instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        Instruction.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

def data(self):

    return{

        'id':self.id,
        'name': self.name,
        'description': self.description,
        'tools': self.tools,
        'cost': self.cost,
        'duration': self.duration,
        'user_id': self.user_id,

    }

@classmethod

def get_all_published(cls):
    return cls.query.filter_by(is_publish=True).all()

@classmethod
def get_by_id(cls,recipe_id):
    return cls.query.filter_by(id=recipe_id).first()

def save(self):
    db.session.add(self)
    db.session.commit()

def delete(self):
    db.session.delete(self)
    db.session.commit()

