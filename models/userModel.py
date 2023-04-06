
from db import db

from sqlalchemy import Column,types
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__="users"

    id=Column(types.Integer,primary_key=True)
    username=Column(types.String(80),nullable=False,unique=True)
    password=Column(types.String(129),nullable=False)    
    email=Column(types.String,unique=True)