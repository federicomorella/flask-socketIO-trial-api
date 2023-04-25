
from db import db
from sqlalchemy import Column,types,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import or_,and_


class User_Contact(db.Model):
    __tablename__="user_contact" 
    id=Column(types.Integer,primary_key=True)
    user_id=Column(types.Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    contact_id=Column(types.Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)     
    
      

class UserModel(db.Model):
    __tablename__="users"
    __allow_unmapped__ = True
    id=Column(types.Integer,primary_key=True)
    username=Column(types.String(80),nullable=False,unique=True)
    password=Column(types.String(129),nullable=False)    
    email=Column(types.String,unique=True)
    rooms:list

    
    contacts = relationship('UserModel', 
        secondary = 'user_contact', 
        primaryjoin = id==User_Contact.user_id, 
        secondaryjoin = id==User_Contact.contact_id,
        backref='followers',
        lazy = 'dynamic')
    
    
    
    def follow(self, user):
        if not self.is_following(user):
            print('append user',user.username,flush=True)
            self.contacts.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.contacts.remove(user)
            return self
    
    def is_following(self, user):
        return user in self.contacts