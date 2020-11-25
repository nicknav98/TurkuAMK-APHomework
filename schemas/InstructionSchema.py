from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema


def validate_cost(n):
    if n < 1:
        raise ValidationError('cost must be greater than 0.')
    if n > 100000:
        raise ValidationError('cost must not be greater than 100,000.')


class InstructionSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    cost = fields.Integer(validate=validate_cost)
    duration = fields.Integer()
    directions = fields.String(validate=[validate.Length(max=1000)])
    is_publish = fields.Boolean(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    @validates('duration')
    def validate_duration(self, value):
        if value < 1:
            raise ValidationError('Duration must be greater than 0.')
        if value > 300:
            raise ValidationError('Cook time must not be greater than 300 days.')
