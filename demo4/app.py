from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages in memory (in production, use a database)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send existing messages to newly connected client
    for message in messages:
        emit('new_message', message)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_message')
def handle_send_message(data):
    message = {
        'text': data['message'],
        'timestamp': data.get('timestamp', '')
    }
    
    # Store the message
    messages.append(message)
    
    # Broadcast to all connected clients
    emit('new_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5004)
