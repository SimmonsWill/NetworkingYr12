from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
socketio = SocketIO(app, async_mode='eventlet')

users = {}        # sid -> { username, room }
taken_nicks = {}  # username (lowercase) -> sid
history = {}      # channel -> [ {user, text, type, time} ]

CHANNELS = ['general', 'announcements', 'gaming', 'tech', 'random']

def record(room, msg):
    history.setdefault(room, []).append(msg)

def now():
    return datetime.now().strftime('%H:%M')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/check_nick')
def check_nick():
    nick = request.args.get('nick', '').strip().lower()
    taken = nick in taken_nicks
    return jsonify({'taken': taken})

@socketio.on('join')
def on_join(data):
    username = data['username'].strip()
    room = data['room']

    if room not in CHANNELS:
        emit('error', {'text': 'Invalid channel.'})
        return

    nick_key = username.lower()
    if nick_key in taken_nicks and taken_nicks[nick_key] != request.sid:
        emit('error', {'text': f'Nickname "{username}" is already taken.'})
        return

    users[request.sid] = {'username': username, 'room': room}
    taken_nicks[nick_key] = request.sid
    join_room(room)

    # Send history to the joining user only
    emit('history', {'room': room, 'messages': history.get(room, [])})

    msg = {'user': 'Server', 'text': f'{username} has joined #{room}', 'type': 'system', 'time': now()}
    record(room, msg)
    emit('message', msg, to=room)
    emit('joined', {'room': room, 'username': username, 'channels': CHANNELS})

@socketio.on('switch_room')
def on_switch_room(data):
    info = users.get(request.sid, {})
    username = info.get('username', 'Unknown')
    old_room = info.get('room')
    new_room = data['room']

    if new_room not in CHANNELS:
        emit('error', {'text': 'Invalid channel.'})
        return

    if old_room:
        leave_room(old_room)
        msg = {'user': 'Server', 'text': f'{username} has left', 'type': 'system', 'time': now()}
        record(old_room, msg)
        emit('message', msg, to=old_room)

    users[request.sid]['room'] = new_room
    join_room(new_room)

    # Send history of new room to the switching user only
    emit('history', {'room': new_room, 'messages': history.get(new_room, [])})

    msg = {'user': 'Server', 'text': f'{username} has joined #{new_room}', 'type': 'system', 'time': now()}
    record(new_room, msg)
    emit('message', msg, to=new_room)
    emit('switched', {'room': new_room})

@socketio.on('message')
def on_message(data):
    info = users.get(request.sid, {})
    username = info.get('username', 'Unknown')
    room = info.get('room', 'general')
    msg = {'user': username, 'text': data['text'], 'type': 'user', 'time': now()}
    record(room, msg)
    emit('message', msg, to=room)

@socketio.on('disconnect')
def on_disconnect():
    info = users.pop(request.sid, {})
    username = info.get('username', 'Unknown')
    room = info.get('room')
    nick_key = username.lower()
    if taken_nicks.get(nick_key) == request.sid:
        del taken_nicks[nick_key]
    if room:
        msg = {'user': 'Server', 'text': f'{username} has left', 'type': 'system', 'time': now()}
        record(room, msg)
        emit('message', msg, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8090, debug=True)
