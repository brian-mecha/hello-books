from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str()
    password=fields.Str()

    def __repr__(self):
        return self.name

class BookSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    author = fields.Str()

    def __repr__(self):
        return self.name