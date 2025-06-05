"""
Demo 3: First Websocket Connection
Introduction to Flask-SocketIO with basic websocket connection and echo functionality.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('echo_message')
def handle_echo_message(data):
    message = data.get('message', '')
    username = data.get('username', 'Anonymous')
    
    print(f'Echo request from {username}: {message}')
    
    # Echo the message back to the sender
    emit('echo_response', {
        'username': username,
        'message': message,
        'echo': True
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5003)
