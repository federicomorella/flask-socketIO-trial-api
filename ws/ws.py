from flask_socketio import SocketIO,emit, ConnectionRefusedError,join_room,leave_room,send
from flask_jwt_extended import decode_token

from flask import request


def socketIO_init(app):
    socketio=SocketIO(app,cors_allowed_origins='*',logger=True)    
    print('socketIO initialized')
    
            
    @socketio.on('connect')
    def test_connect(auth):
        print('WS on connection----------------')
        print('request',request.sid)
        print(auth)
        if decode_token(auth["token"]):
            emit('my response', {'data': 'Connected'})
            print('WS Client connected',auth)
        else:
            raise ConnectionRefusedError('unauthorized!')

    @socketio.on('disconnect')
    def test_disconnect():
        print('WS Client disconnected')
    
    
        
    @socketio.on('MyMessage')
    def handle_json(data):
        print('MyMessage----------------')
        print(request.sid)
        print('Received json: '+ str(data))
        emit('server_message',data,to='1234',include_self=False)
        
    
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
        emit('room_leave',username + ' has left the room.', to=room)
        
        
    return socketio
 