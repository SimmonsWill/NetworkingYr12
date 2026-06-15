from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
socketio = SocketIO(app, async_mode='eventlet')

users = {}   # sid -> { username, room }

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    users[request.sid] = {'username': username, 'room': room}
    join_room(room)
    emit('message', {
        'user': 'Server',
        'text': f'{username} has joined #{room}',
        'type': 'system'
    }, to=room)
    emit('room_info', {'room': room, 'username': username})

@socketio.on('message')
def on_message(data):
    info = users.get(request.sid, {})
    username = info.get('username', 'Unknown')
    room = info.get('room', data.get('room', 'general'))
    emit('message', {
        'user': username,
        'text': data['text'],
        'type': 'user'
    }, to=room)

@socketio.on('disconnect')
def on_disconnect():
    info = users.pop(request.sid, {})
    username = info.get('username', 'Unknown')
    room = info.get('room')
    if room:
        emit('message', {
            'user': 'Server',
            'text': f'{username} has left',
            'type': 'system'
        }, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8090, debug=True)
