# SocketIO Trial project
This is a flask trial project to perform user login, JWT authentication, websocket connection using Flask-SocketIO and SQLAlchemy connected to a postgres database.

I have a sample react app in 
[this](https://github.com/federicomorella/flask-socketIO-trial-ui)
repository that you can use

### Configuration
A .env-example file is provided that contain the necesary environment variables for the API.

### Database
The app uses alembic for database migrations. You can use this command to initialize migrations folder:
``` console
flask db init
```
Create a new migration based on the current models:
``` console
flask db migrate
```
Then update database:
``` console
flask db upgrade
```

### Run application
A docker-compose file is provided to run the application locally:
``` console
docker compose up -d
```

For running app in production use:
``` console
gunicorn -b :PORT "app:create_app()"
```


### API documentation
_[API_URL]/swagger-ui_ shows the API documentation of the running app

### Live demo
A web service automatically deploy tha API to https://flask-socketio.onrender.com 