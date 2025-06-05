from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store data in memory (in production, use a database)
rooms = {
    'general': {'messages': [], 'users': {}},
    'random': {'messages': [], 'users': {}},
    'tech': {'messages': [], 'users': {}}
}
typing_users = {}  # room -> {user_id: timestamp}

@app.route('/')
def index():
    return render_template('index.html', rooms=list(rooms.keys()))

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    
    # Remove user from all rooms and notify others
    for room_name, room_data in rooms.items():
        if request.sid in room_data['users']:
            user = room_data['users'][request.sid]
            del room_data['users'][request.sid]
            
            # Remove from typing indicators
            if room_name in typing_users and request.sid in typing_users[room_name]:
                del typing_users[room_name][request.sid]
                emit('typing_update', list(typing_users[room_name].values()), room=room_name)
            
            # Create leave notification
            leave_message = {
                'type': 'system',
                'text': f"{user['nickname']} left {room_name}",
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'room': room_name
            }
            
            # Add to room history and broadcast
            room_data['messages'].append(leave_message)
            emit('user_left', leave_message, room=room_name)
            emit('user_list_update', {
                'room': room_name,
                'users': list(room_data['users'].values())
            }, room=room_name)

@socketio.on('join_room')
def handle_join_room(data):
    nickname = data.get('nickname', 'Anonymous').strip()
    room_name = data.get('room', 'general')
    
    if not nickname:
        nickname = 'Anonymous'
    
    if room_name not in rooms:
        room_name = 'general'
    
    # Join the socket room
    join_room(room_name)
    
    # Store user info
    rooms[room_name]['users'][request.sid] = {
        'id': request.sid,
        'nickname': nickname,
        'joined_at': datetime.now().strftime('%H:%M:%S'),
        'room': room_name
    }
    
    # Send existing messages to newly connected client
    for message in rooms[room_name]['messages']:
        emit('new_message', message)
    
    # Create join notification
    join_message = {
        'type': 'system',
        'text': f"{nickname} joined {room_name}",
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'room': room_name
    }
    
    # Add join message to history
    rooms[room_name]['messages'].append(join_message)
    
    # Broadcast join notification and updated user list
    emit('user_joined', join_message, room=room_name)
    emit('user_list_update', {
        'room': room_name,
        'users': list(rooms[room_name]['users'].values())
    }, room=room_name)
    
    # Send room list to user
    emit('room_list_update', list(rooms.keys()))

@socketio.on('switch_room')
def handle_switch_room(data):
    old_room = data.get('old_room')
    new_room = data.get('new_room', 'general')
    
    if new_room not in rooms:
        new_room = 'general'
    
    # Leave old room
    if old_room and old_room in rooms and request.sid in rooms[old_room]['users']:
        user = rooms[old_room]['users'][request.sid]
        del rooms[old_room]['users'][request.sid]
        leave_room(old_room)
        
        # Remove from typing indicators
        if old_room in typing_users and request.sid in typing_users[old_room]:
            del typing_users[old_room][request.sid]
            emit('typing_update', list(typing_users[old_room].values()), room=old_room)
        
        # Create leave notification
        leave_message = {
            'type': 'system',
            'text': f"{user['nickname']} left {old_room}",
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'room': old_room
        }
        
        rooms[old_room]['messages'].append(leave_message)
        emit('user_left', leave_message, room=old_room)
        emit('user_list_update', {
            'room': old_room,
            'users': list(rooms[old_room]['users'].values())
        }, room=old_room)
    
    # Join new room
    join_room(new_room)
    nickname = data.get('nickname', 'Anonymous')
    
    rooms[new_room]['users'][request.sid] = {
        'id': request.sid,
        'nickname': nickname,
        'joined_at': datetime.now().strftime('%H:%M:%S'),
        'room': new_room
    }
    
    # Send existing messages to client
    for message in rooms[new_room]['messages']:
        emit('new_message', message)
    
    # Create join notification
    join_message = {
        'type': 'system',
        'text': f"{nickname} joined {new_room}",
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'room': new_room
    }
    
    rooms[new_room]['messages'].append(join_message)
    emit('user_joined', join_message, room=new_room)
    emit('user_list_update', {
        'room': new_room,
        'users': list(rooms[new_room]['users'].values())
    }, room=new_room)

@socketio.on('send_message')
def handle_send_message(data):
    room_name = data.get('room', 'general')
    
    if room_name not in rooms or request.sid not in rooms[room_name]['users']:
        return  # User not properly joined
    
    user = rooms[room_name]['users'][request.sid]
    message_text = data['message'].strip()
    
    # Check for private message (whisper)
    if message_text.startswith('/whisper ') or message_text.startswith('/w '):
        parts = message_text.split(' ', 2)
        if len(parts) >= 3:
            command, target_nickname, private_message = parts
            
            # Find target user in current room
            target_user = None
            for user_id, user_info in rooms[room_name]['users'].items():
                if user_info['nickname'].lower() == target_nickname.lower():
                    target_user = user_info
                    break
            
            if target_user:
                # Send private message to both sender and recipient
                whisper_message = {
                    'type': 'whisper',
                    'text': private_message,
                    'from_nickname': user['nickname'],
                    'to_nickname': target_user['nickname'],
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'room': room_name
                }
                
                # Send to sender
                emit('private_message', whisper_message)
                # Send to recipient
                emit('private_message', whisper_message, room=target_user['id'])
            else:
                # User not found
                error_message = {
                    'type': 'system',
                    'text': f"User '{target_nickname}' not found in this room",
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'room': room_name
                }
                emit('new_message', error_message)
            return
    
    # Regular public message
    message = {
        'type': 'user',
        'text': message_text,
        'nickname': user['nickname'],
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'user_id': request.sid,
        'room': room_name
    }
    
    # Store the message
    rooms[room_name]['messages'].append(message)
    
    # Keep only last 100 messages per room to prevent memory issues
    if len(rooms[room_name]['messages']) > 100:
        rooms[room_name]['messages'].pop(0)
    
    # Remove user from typing indicators
    if room_name in typing_users and request.sid in typing_users[room_name]:
        del typing_users[room_name][request.sid]
        emit('typing_update', list(typing_users[room_name].values()), room=room_name)
    
    # Broadcast to all users in the room
    emit('new_message', message, room=room_name)

@socketio.on('typing_start')
def handle_typing_start(data):
    room_name = data.get('room', 'general')
    
    if room_name not in rooms or request.sid not in rooms[room_name]['users']:
        return
    
    user = rooms[room_name]['users'][request.sid]
    
    # Add user to typing indicators
    if room_name not in typing_users:
        typing_users[room_name] = {}
    
    typing_users[room_name][request.sid] = user['nickname']
    
    # Broadcast typing update to room (excluding sender)
    emit('typing_update', list(typing_users[room_name].values()), room=room_name, include_self=False)

@socketio.on('typing_stop')
def handle_typing_stop(data):
    room_name = data.get('room', 'general')
    
    if room_name in typing_users and request.sid in typing_users[room_name]:
        del typing_users[room_name][request.sid]
        
        # Broadcast typing update to room
        emit('typing_update', list(typing_users[room_name].values()), room=room_name)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5006)
