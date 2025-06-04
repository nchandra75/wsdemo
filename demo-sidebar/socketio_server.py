"""
Flask-SocketIO Echo Server
This shows how much simpler the same functionality is with Flask-SocketIO!
Compare this to the raw WebSocket version.
"""

from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple HTML template (inline for simplicity)
CLIENT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask-SocketIO Echo Client</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            font-weight: bold;
        }
        .connected { background-color: #d4edda; color: #155724; }
        .disconnected { background-color: #f8d7da; color: #721c24; }
        
        #messages {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
            background-color: #fafafa;
        }
        .message {
            margin: 5px 0;
            padding: 5px;
            border-radius: 3px;
        }
        .sent { background-color: #e3f2fd; }
        .received { background-color: #f3e5f5; }
        
        input[type="text"] {
            width: 70%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Flask-SocketIO Echo Client</h1>
        <p><strong>Notice:</strong> Much simpler code! SocketIO handles all the connection complexity.</p>
        
        <div id="status" class="status disconnected">Connecting...</div>
        
        <div id="messages"></div>
        
        <div>
            <input type="text" id="messageInput" placeholder="Type your message here...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        // Initialize SocketIO connection (so much simpler!)
        const socket = io();

        const statusDiv = document.getElementById('status');
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');

        function addMessage(message, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.innerHTML = `<strong>${new Date().toLocaleTimeString()}:</strong> ${message}`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Connection events (automatic!)
        socket.on('connect', function() {
            statusDiv.textContent = 'Connected';
            statusDiv.className = 'status connected';
            addMessage('Connected to server', 'received');
        });

        socket.on('disconnect', function() {
            statusDiv.textContent = 'Disconnected';
            statusDiv.className = 'status disconnected';
            addMessage('Disconnected from server', 'received');
        });

        // Listen for echo responses
        socket.on('echo_response', function(data) {
            addMessage(`Echo: ${data.message}`, 'received');
        });

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                // Send message to server
                socket.emit('echo_message', {message: message});
                addMessage(message, 'sent');
                messageInput.value = '';
            }
        }

        // Allow Enter key to send message
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the client page"""
    return render_template_string(CLIENT_TEMPLATE)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('echo_message')
def handle_echo_message(data):
    """Handle echo message - this is all we need!"""
    message = data.get('message', '')
    logger.info(f"Echoing message: {message}")
    
    # Send the echo back to the client
    emit('echo_response', {
        'message': f"Server says: {message}",
        'timestamp': data.get('timestamp', '')
    })

if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO server on localhost:5000")
    socketio.run(app, host='localhost', port=5000, debug=True)
