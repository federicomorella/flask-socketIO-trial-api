
from db import db
from sqlalchemy import Column,types,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import or_,and_  
from sqlalchemy.sql import func
class MessagesModel(db.Model):
    __tablename__="messages"
    __allow_unmapped__ = True
    id=Column(types.Integer,primary_key=True)
    room_id=Column(types.Integer,ForeignKey('rooms.id',ondelete='CASCADE'),nullable=False)
    user_id=Column(types.Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    message=Column(types.String())
    datetime=Column(types.DateTime(timezone=True),server_default=func.now())