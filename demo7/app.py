from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Data structures
messages = []
users = {}  # session_id -> user_info
polls = {}  # poll_id -> poll_data
reactions = {}  # message_id -> {emoji: count}
collaborative_canvas = []  # list of drawing actions

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'User connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        user = users[request.sid]
        print(f'User disconnected: {user["username"]}')
        
        # Notify others that user left
        emit('user_left', {
            'username': user['username'],
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }, broadcast=True)
        
        del users[request.sid]
        
        # Update user list
        emit('user_list_update', {
            'users': [user['username'] for user in users.values()]
        }, broadcast=True)

@socketio.on('join_chat')
def handle_join_chat(data):
    username = data['username']
    users[request.sid] = {
        'username': username,
        'joined_at': time.time()
    }
    
    # Send existing messages to new user
    emit('message_history', {'messages': messages})
    
    # Send existing polls to new user
    emit('poll_history', {'polls': list(polls.values())})
    
    # Notify others that user joined
    emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, broadcast=True)
    
    # Update user list for everyone
    emit('user_list_update', {
        'users': [user['username'] for user in users.values()]
    }, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    if request.sid not in users:
        return
    
    user = users[request.sid]
    message_id = f"msg_{len(messages)}_{int(time.time())}"
    
    message = {
        'id': message_id,
        'username': user['username'],
        'message': data['message'],
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    messages.append(message)
    reactions[message_id] = {}
    
    emit('new_message', message, broadcast=True)

@socketio.on('create_poll')
def handle_create_poll(data):
    if request.sid not in users:
        return
    
    user = users[request.sid]
    poll_id = f"poll_{len(polls)}_{int(time.time())}"
    
    poll = {
        'id': poll_id,
        'question': data['question'],
        'options': data['options'],
        'creator': user['username'],
        'votes': {option: [] for option in data['options']},
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    polls[poll_id] = poll
    emit('new_poll', poll, broadcast=True)

@socketio.on('vote_poll')
def handle_vote_poll(data):
    if request.sid not in users:
        return
    
    user = users[request.sid]
    poll_id = data['poll_id']
    option = data['option']
    
    if poll_id not in polls:
        return
    
    poll = polls[poll_id]
    
    # Remove user's previous vote if any
    for opt in poll['votes']:
        if user['username'] in poll['votes'][opt]:
            poll['votes'][opt].remove(user['username'])
    
    # Add new vote
    if option in poll['votes']:
        poll['votes'][option].append(user['username'])
    
    emit('poll_updated', poll, broadcast=True)

@socketio.on('add_reaction')
def handle_add_reaction(data):
    if request.sid not in users:
        return
    
    user = users[request.sid]
    message_id = data['message_id']
    emoji = data['emoji']
    
    if message_id not in reactions:
        return
    
    if emoji not in reactions[message_id]:
        reactions[message_id][emoji] = []
    
    # Toggle reaction (add if not present, remove if present)
    if user['username'] in reactions[message_id][emoji]:
        reactions[message_id][emoji].remove(user['username'])
        if not reactions[message_id][emoji]:
            del reactions[message_id][emoji]
    else:
        reactions[message_id][emoji].append(user['username'])
    
    emit('reaction_updated', {
        'message_id': message_id,
        'reactions': reactions[message_id]
    }, broadcast=True)

@socketio.on('canvas_draw')
def handle_canvas_draw(data):
    if request.sid not in users:
        return
    
    user = users[request.sid]
    
    draw_action = {
        'type': data['type'],  # 'start', 'draw', 'end'
        'x': data['x'],
        'y': data['y'],
        'color': data.get('color', '#000000'),
        'username': user['username'],
        'timestamp': time.time()
    }
    
    collaborative_canvas.append(draw_action)
    
    # Broadcast to all other users (not the sender)
    emit('canvas_update', draw_action, broadcast=True, include_self=False)

@socketio.on('clear_canvas')
def handle_clear_canvas():
    if request.sid not in users:
        return
    
    user = users[request.sid]
    collaborative_canvas.clear()
    
    emit('canvas_cleared', {
        'username': user['username']
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5007)
