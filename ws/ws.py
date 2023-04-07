from flask_socketio import SocketIO,emit, ConnectionRefusedError
from flask_jwt_extended import decode_token


def socketIO_init(app):
    socketio=SocketIO(app,cors_allowed_origins='*')    
    print('socketIO initialized',flush=True)
    
            
    @socketio.on('connect')
    def test_connect(auth):
        print('WS on connection----------------')
        print(auth,flush=True)
        if decode_token(auth["token"]):
            emit('my response', {'data': 'Connected'})
            print('WS Client connected',auth,flush=True)
        else:
            raise ConnectionRefusedError('unauthorized!')

    @socketio.on('disconnect')
    def test_disconnect():
        print('WS Client disconnected')
    
    
        
    @socketio.on('MyMessage')
    def handle_json(json):
        print('MyMessage----------------')
        print('received json: ' + str(json),flush=True)
        
 