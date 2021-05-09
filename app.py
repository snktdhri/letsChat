from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from datetime import datetime
import redis_utils as rutils
import eventlet
import logging
try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random!@#@str'
socketio = SocketIO(app, cors_allowed_origins='*')

MSGS= []

logging.basicConfig(filename='logs/app.log', level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        messages = get_messages(room)
        app.logger.info("messages: {}", messages)
        return render_template('chat.html', messages= messages, username=username, room=room)
    else:
        return "Room not found", 404


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data)
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

def save_message_mem(room, msg, username, date):
    global MSGS
    MSGS.append({
    "room" : room,
    "message" : msg,
    "created_at" : date,
    "username" : username
    })

def save_message(data):
    msg = json.dumps(data)
    rutils.add_to_list(data["room"], msg)

def get_messages(room):
    ls = rutils.get_list_contents(room)
    app.logger.info("ls {} {} {}", type(ls), len(ls), ls)
    print (ls)
    return [json.loads(msg) for msg in rutils.get_list_contents(room)]

def get_messages_mem(room):
    return [msg  for msg in MSGS if msg["room"] == room]


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False)