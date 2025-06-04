from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages and users in memory (in production, use a database)
messages = []
users = {}  # session_id -> user_info

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    
    # Remove user from users list and notify others
    if request.sid in users:
        user = users[request.sid]
        del users[request.sid]
        
        # Create leave notification
        leave_message = {
            'type': 'system',
            'text': f"{user['nickname']} left the chat",
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'user_count': len(users)
        }
        
        # Broadcast leave notification and updated user list
        emit('user_left', leave_message, broadcast=True)
        emit('user_list_update', list(users.values()), broadcast=True)

@socketio.on('join_chat')
def handle_join_chat(data):
    nickname = data.get('nickname', 'Anonymous').strip()
    if not nickname:
        nickname = 'Anonymous'
    
    # Store user info
    users[request.sid] = {
        'id': request.sid,
        'nickname': nickname,
        'joined_at': datetime.now().strftime('%H:%M:%S')
    }
    
    # Send existing messages to newly connected client
    for message in messages:
        emit('new_message', message)
    
    # Create join notification
    join_message = {
        'type': 'system',
        'text': f"{nickname} joined the chat",
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'user_count': len(users)
    }
    
    # Add join message to history
    messages.append(join_message)
    
    # Broadcast join notification and updated user list
    emit('user_joined', join_message, broadcast=True)
    emit('user_list_update', list(users.values()), broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    if request.sid not in users:
        return  # User not properly joined
    
    user = users[request.sid]
    message = {
        'type': 'user',
        'text': data['message'],
        'nickname': user['nickname'],
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'user_id': request.sid
    }
    
    # Store the message
    messages.append(message)
    
    # Keep only last 100 messages to prevent memory issues
    if len(messages) > 100:
        messages.pop(0)
    
    # Broadcast to all connected clients
    emit('new_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5005)
