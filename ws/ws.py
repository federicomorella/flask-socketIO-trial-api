from flask_socketio import socketio,emit


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json),flush=True)
    
    
@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')