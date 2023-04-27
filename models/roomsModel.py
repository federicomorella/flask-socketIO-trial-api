
from db import db
from sqlalchemy import Column,types,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import or_,and_
from models import UserModel

class Room_contact(db.Model):
    __tablename__="room_contact" 
    id=Column(types.Integer,primary_key=True)
    room_id=Column(types.Integer,ForeignKey('rooms.id',ondelete="CASCADE"),nullable=False)
    contact_id=Column(types.Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)     
    
      

class RoomModel(db.Model):
    __tablename__="rooms"
    __allow_unmapped__ = True
    id=Column(types.Integer,primary_key=True)
    name=Column(types.String(80),nullable=False)

    users = relationship('UserModel', 
        secondary = 'room_contact',
        backref='rooms',
        lazy = 'dynamic')
    
    messages:list
    

    def addUser(self,user:UserModel):
        '''add user to room
        return True on success or False if fails'''
        print(f'Adding {user.username} to room {self.id}...',flush=True)
        if user not in self.users:
            
            self.users.append(user)
            try:
                db.session.commit()
                return True
            except:
                return False
                
        
    
    def removeUser(self,user):
        '''remove user from room
        return True on success or False if fails'''
        if user in self.users:
            try:
                self.users.remove(user)            
                db.session.commit()
                return True
            except:
                return False
            

        
        