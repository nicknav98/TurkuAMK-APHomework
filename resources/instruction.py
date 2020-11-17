from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.instructions import Instruction, instruction_list



class InstructionListResource(Resource):

    def get(self):

        data = []

        for INSTRUCTION in instruction_list:
            if INSTRUCTION.is_publish is True:
                data.append(INSTRUCTION.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        INSTRUCTION = Instruction(name=data['name'],
                        description=data['description'],
                        steps=data['steps'],
                        tools=data['tools'],
                        cost=data['cost'],
                        duration=data['duration'])

        instruction_list.append(Instruction)

        return Instruction.data, HTTPStatus.CREATED


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

