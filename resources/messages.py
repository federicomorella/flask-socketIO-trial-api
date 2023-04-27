from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask_jwt_extended import create_access_token,jwt_required, \
    get_jwt, get_jwt_identity

from db import db
from sqlalchemy import select ,delete
from sqlalchemy.orm import load_only
from sqlalchemy.sql import or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import RoomModel,UserModel,MessagesModel
from schemas import MessageSchema,NewMessageSchema

blp=Blueprint("messages",__name__,description="operations on messages")


@blp.route('/rooms/<int:room_id>/messages')
class messages(MethodView):
    
    @blp.arguments(NewMessageSchema)
    @jwt_required()
    def post(self,message_data,room_id):
        '''post new message to the room''' 
        room:RoomModel=db.get_or_404(RoomModel,room_id)
        user=db.get_or_404(UserModel,get_jwt_identity())
        
        if user in room.users:
            message=MessagesModel(room_id=room_id,user_id=get_jwt_identity(),message=message_data.get('message'))
            try:
                db.session.add(message)
                db.session.commit()
            except Exception as e:
                abort(500,message=f'Failed to create message: {str(e)}')
        else:
            abort(401,message="Can not send message if you are not in the room")
        
        return {'message':'Message created'}
        
            
            
            
            
    @blp.response(200,MessageSchema(many=True))
    @jwt_required()
    def get(self,room_id):
        messages=db.session.query(MessagesModel).filter(MessagesModel.room_id==room_id)
        return messages
        
        

        
        
    
  