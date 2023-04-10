#!/bin/sh
if [ ! -d "./data" ] 
then
    flask db init
    flask db migrate
fi


echo "initializing database..."
flask db upgrade

echo "Starting application"
# flask run --host '0.0.0.0'
# gunicorn -b :5000 "app:create_app()"
# python app.py
top