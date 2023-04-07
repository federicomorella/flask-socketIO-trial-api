import os #lo uso para levantar las variables de entrono
from flask import Flask,request,jsonify,render_template
from flask_smorest import Api

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from db import db
from models import * #importo los modelos para que los use sqlalchemy
from resources.users import blp as UserBlp

from dotenv import load_dotenv

from ws.ws import socketIO_init

def create_app(db_url=None):

    load_dotenv()
    app=Flask(__name__,
            static_url_path='', 
            static_folder='static')
    
    CORS(app)
    app.config["PROPAGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"]="Travel's Agents API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    #defino la conexion a la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

    #JWT
    app.config["JWT_SECRET_KEY"]=os.getenv("SECRET",'my_secret_key')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]=600
    jwt=JWTManager(app)

    #SocketIO
    app.config['SECRET_KEY'] = os.getenv("SECRET",'my_secret_key')
    # Initialize socketIO events inside ws.py
    socketIO_init(app)

    db.init_app(app) #inicializa la conexión con la base de datos

    migrate=Migrate(app,db)
    

    api=Api(app)
    
    API_PREFIX='/v1'
    api.register_blueprint(UserBlp,url_prefix=API_PREFIX)
    return app
