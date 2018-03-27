from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    password=fields.Str()

    def __repr__(self):
        return self.name