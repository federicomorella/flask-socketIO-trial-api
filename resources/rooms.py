from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,jwt_required, \
    get_jwt, get_jwt_identity

from db import db
from sqlalchemy import select ,delete
from sqlalchemy.orm import load_only
from sqlalchemy.sql import or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import RoomModel,UserModel
from schemas import UserLoginSchema,UserSchema,ContactSchema,RoomSchema,PlainRoomSchema,PlainUserSchema

blp=Blueprint("rooms",__name__,description="operations on rooms")


@blp.route('/rooms')
class Rooms(MethodView):
    
    @blp.response(200,UserSchema)
    @jwt_required()
    def get(self):
        '''return all current user's rooms {"rooms":[]}'''
        user:UserModel=db.get_or_404(UserModel,get_jwt_identity())   
        return {'rooms':user.rooms}
    
    
    
    @blp.arguments(PlainRoomSchema)
    @blp.response(200,RoomSchema)
    @jwt_required()
    def post(self,room_data):
        '''create new room
        append current user to the room
        return created room'''
        try:
            room=RoomModel(**room_data)
            db.session.add(room)
            db.session.commit()
            user=db.get_or_404(UserModel,get_jwt_identity())
            room.addUser(user)
            return room
            
        except SQLAlchemyError:
            abort(409,message='Failed to create new room')
        except:
            abort(500,message='Failed to create new room')
        

@blp.route('/rooms/<int:room_id>')
class room_operation(MethodView):
    @jwt_required()
    @blp.response(200,PlainRoomSchema)    
    def get(self,room_id):
        '''return room details without users'''
        room=db.get_or_404(RoomModel,room_id)
        return room
    
    @jwt_required()
    def delete(self,room_id):
        '''remove current user from the room'''
        room:RoomModel=db.get_or_404(RoomModel,room_id)
        user=db.get_or_404(UserModel,get_jwt_identity())
        res=False
        if user:
            res=room.removeUser(user)
        if res:
            return {'message':f'current user removed from room {room_id}'},200
        else:
            return {'message':f'Failed to remove from room {room_id}'},500
        



@blp.route('/rooms/<int:room_id>/contacts')
class Rooms_id(MethodView):
    @jwt_required()
    @blp.response(200,RoomSchema)
    def get(self,room_id):
        '''get room contacts
        return 401 if current user is not in the room'''
        room:RoomModel=db.get_or_404(RoomModel,room_id)      
        user:UserModel=db.session.query(UserModel).with_entities(UserModel.username).filter(UserModel.id==get_jwt_identity()).one()
        if user.username not in map(lambda u:u.username, room.users):
            abort(401,message=f'User does not belong to room {room_id}')
        return {'users':room.users}
    
    
    @jwt_required()
    @blp.arguments(PlainUserSchema)
    def post(self,user_data,room_id):
        '''add user to the room. Only a user from the room can add new users.
        user={"username":"name"}'''
        room:RoomModel=db.get_or_404(RoomModel,room_id) 
        user:UserModel=db.session.query(UserModel).filter(UserModel.username==user_data.get("username")).first()
        current_user=db.get_or_404(UserModel,get_jwt_identity())
        if current_user in room.users:
            if not user:
                abort(404,message='User not found')
            
            if room.addUser(user):
                return {'message':'user added to the room'}
            else:
                abort(500,message='Failed to add user')
        else:
            abort(401,message='Only users from the room can add new users')
        
      

