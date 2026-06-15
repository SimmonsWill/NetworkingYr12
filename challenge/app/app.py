from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
socketio = SocketIO(app, async_mode='eventlet')

users = {}  # maps session id -> username

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    users[request.sid] = data['username']
    join_room(data['room'])
    emit('message', {
        'user': 'Server',
        'text': f"{data['username']} joined #{data['room']}"
    }, to=data['room'])

@socketio.on('message')
def on_message(data):
    username = users.get(request.sid, 'Unknown')
    emit('message', {
        'user': username,
        'text': data['text']
    }, to=data['room'])

@socketio.on('disconnect')
def on_disconnect():
    username = users.pop(request.sid, 'Unknown')
    emit('message', {
        'user': 'Server',
        'text': f'{username} has left'
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8090)
