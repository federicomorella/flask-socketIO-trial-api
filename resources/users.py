from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,jwt_required, \
    get_jwt, get_jwt_identity

from db import db
from sqlalchemy import select 
from sqlalchemy.sql import or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import UserModel
from schemas import UserLoginSchema,UserSchema

blp=Blueprint("users",__name__,description="operations on users")

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self,user_data):
        '''login user using username and password'''
        user:UserModel=db.session.query(UserModel).filter(UserModel.username==user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token=create_access_token(identity=user.id,fresh=True)
            return {"access_token":access_token}
        else:
            abort(401,message="invalid credentials.")
        


@blp.route('/signup')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        '''register new user'''
        
        #hash password to store in db
        user_data={**user_data,
            "password":pbkdf2_sha256.hash(user_data["password"])
            }
        
        #create new user
        user=UserModel(**user_data)
        
        
        try: #try to insert user in db.
            db.session.add(user)
            db.session.commit()
        except IntegrityError as ie:
            abort( 409,message="Username or email already exists")
        except SQLAlchemyError:
            abort(500,message="Failed to register user")
        else:
            return {"message": "User created"},201


@blp.route('/user')
class AgentList(MethodView):   
    
    @jwt_required()
    @blp.arguments(UserSchema)
    def put(self,user_data):
        '''modify current user data'''
        #obtain user id from jwt subject
        user:UserModel=db.get_or_404(UserModel,get_jwt().get("sub"))
        
        #update fields
        user.email=user_data.get('email') or user.email
        
        if user_data.get('password'):
            user.password=pbkdf2_sha256.hash(user_data["password"])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as ie:
            abort( 409,message="Email alredy registered for another user")
        except SQLAlchemyError:
            abort(500,message="Failed to update user information")
        else:
            return {"message": "User updated"},201