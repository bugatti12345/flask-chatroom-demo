
# Copy of http://stackoverflow.com/a/20104705
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet

app = Flask(__name__, template_folder='templates')
app.debug = True

socketio = SocketIO(app, ping_timeout=5)
# socketio.init_app(app, cors_allowed_origins="*")
# eventlet.monkey_patch()

room_list = {
    '1001': 'General',
    '1002': 'Games',
    '1003': 'Study'
}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/frontdesk', methods=['GET'])
def frontdesk():
    return render_template('frontdesk.html', title="Frontdesk System")


@app.route('/client', methods=['GET'])
def client():
    return render_template('frontdesk.html', title="Customer Service")


@socketio.on('my event')
def test_message(message):
    print(message)
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event')
def test_broadcast(message):
    print(message)
    if message.get('user'):
        emit('response', {'data': message['data'], 'user': message['user']}, broadcast=True)
    else:
        emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('join')
def on_join(data):
    print(data)
    username = data['username']
    room = data['room']
    join_room(room)
    # send(username + ' has entered the room.', to=room)
    emit('my response', {'data': username + ' has entered the room.', 'user': username}, to=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


@socketio.on('my room event')
def on_my_room_event(data):
    print(data)
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('my ping')
def test_connect():
    emit('my ping')


if __name__ == '__main__':
    socketio.run(app, port=5001)
    # eventlet.serve(eventlet.listen(('127.0.0.1', 5001)), app)