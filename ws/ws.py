from flask_socketio import SocketIO,emit, ConnectionRefusedError,join_room,leave_room,send
from flask_jwt_extended import decode_token

from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import UserModel

from flask import request
import json
   
socket_clients=dict()

def socketIO_init(app):
    socketio:SocketIO=SocketIO(app,cors_allowed_origins='*',logger=True)    
    print('socketIO initialized')
 
            
    @socketio.on('connect')
    def test_connect(auth):
        print('WS on connection----------------')
        print('SID:',request.sid)
        decoded_token=decode_token(auth["token"])
        if decoded_token:
            emit('my response', {'data': 'Connected'})
            
            #Add client to the dictionary
            user=db.get_or_404(UserModel,decoded_token.get('sub'))
            socket_clients[user.username]=request.sid            
            print('Clients: ',socket_clients)
            
            #join rooms
            _join_all_rooms(user)
            
        else:
            raise ConnectionRefusedError('unauthorized!')

    @socketio.on('disconnect')
    def test_disconnect():
        print('WS Client disconnecting-----------')
        #remove client from the dictionary
        SID=request.sid
        client=[k for k,v in socket_clients.items() if v==SID]
        print(client[0])
        if client:
            socket_clients.pop(client[0])
        

    
    
        
    @socketio.on('MyMessage')
    def handle_json(data):
        print('MyMessage----------------')
        print(request.sid)
        print('Received json: '+ str(data))
        emit('server_message',data,to=data.get('room'),include_self=False)
        
    
    @socketio.on('join')
    def on_join(data):
        print('--------------join----------------------')
        print('data:',data)
        username = data['username']
        room = data['room']
        join_room(room)
        print(username + ' has entered the room.')
        emit('room_enter',username + ' has entered the room.', to=room)
        

    @socketio.on('leave')
    def on_leave(data): 
        print('--------------leave----------------------')
        username = data['username']
        room = data['room']
        leave_room(room)
        emit('room_leave',f'{username} has entered the room `{room.name}`', to=room)
        
        
    def _join_all_rooms(user:UserModel):
        '''join user to all his rooms'''
        for room in user.rooms:
            join_room(room.id)
            print(f'{user.username} entering room `{room.name}`')
            socketio.emit('room_enter', f'{user.username} has entered the room `{room.name}`', to=room.id)
        return
    
            
        
    return socketio
 
 
    