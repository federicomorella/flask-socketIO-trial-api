from marshmallow import Schema,fields


class PlainUserSchema(Schema):
    '''{username,email}'''    
    username=fields.String()
    email=fields.String()
    
class PlainRoomSchema(Schema):
    '''{id,name}'''
    id=fields.Integer(dump_only=True)
    name=fields.String(required=True)    
    
class RoomSchema(PlainRoomSchema):
    '''{id,name,users}'''
    users=fields.List(fields.Nested(PlainUserSchema))
    
    
class NewMessageSchema(Schema):
    '''{message}'''
    message=fields.String(required=True)
    
class MessageSchema(Schema):
    '''{id,room_id,username,message,datetime}'''
    id=fields.Integer()
    room_id=fields.Integer()
    username=fields.String()
    message=fields.String()
    datetime=fields.DateTime()
      
    
    
class UserSchema(Schema):
    '''{email,password,name,contacts,rooms}'''    
    username=fields.String()
    password=fields.String(load_only=True)
    email=fields.String()
    contacts=fields.List(fields.Nested(PlainUserSchema))
    rooms=fields.List(fields.Nested(PlainRoomSchema))
    
class UserLoginSchema(Schema):
    '''{email,password}'''
    username=fields.String(required=True)
    password=fields.String(required=True,load_only=True)
    
class ContactSchema(Schema):
    '''{username}'''
    username=fields.String(required=True)