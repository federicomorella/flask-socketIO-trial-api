from marshmallow import Schema,fields

class PlainUserSchema(Schema):
    '''{username,email}'''    
    username=fields.String()
    email=fields.String()
    
    
class UserSchema(Schema):
    '''{email,password,name,instagram}'''    
    username=fields.String()
    password=fields.String(load_only=True)
    email=fields.String()
    contacts=fields.List(fields.Nested(PlainUserSchema))
    
class UserLoginSchema(Schema):
    '''{email,password}'''
    username=fields.String(required=True)
    password=fields.String(required=True,load_only=True)
    
class ContactSchema(Schema):
    '''{username}'''
    username=fields.String(required=True)