from marshmallow import Schema,fields

class UserSchema(Schema):
    '''{email,password,name,instagram}'''    
    username=fields.String()
    password=fields.String()
    email=fields.String()
    
class UserLoginSchema(Schema):
    '''{email,password}'''
    username=fields.String(required=True)
    password=fields.String(required=True,load_only=True)