from marshmallow import Schema, fields, ValidationError, validates_schema


class UserSchema(Schema):
    id = fields.Integer()
    login = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    reg_date = fields.Date(dump_only=True)

    @validates_schema
    def get_auth_method(self, schema):
        if 'email' in schema:
            auth_method = schema['email']
        elif 'login' in schema:
            auth_method = schema['login']
        else:
            raise ValidationError('no available auth method')
        return auth_method
