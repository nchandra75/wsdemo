---
marp: true
theme: default
paginate: true
---

# Fun with Websockets
## Building Real-time Web Applications

---

# What We'll Build Today

- Start with basic web server concepts
- Add forms and user interaction
- Introduce websockets for real-time communication
- Build a complete chat application
- Add advanced features like typing indicators

---

# How Web Servers Work

## Traditional HTTP Request/Response

```
Browser ──── HTTP Request ────► Server
        ◄─── HTTP Response ─── 
```

- Client sends request
- Server processes and responds
- Connection closes
- **One-way communication**

---

# Demo 1: Basic Flask Server

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
```

**Let's run this and see it in action!**

---

# What Just Happened?

1. Flask creates a web server
2. Browser requests a page (`GET /`)
3. Server responds with HTML
4. Connection closes
5. **Static content only**

---

# Demo 2: Adding Forms

```python
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    messages.append({
        'text': message,
        'timestamp': datetime.now()
    })
    return redirect('/')
```

**Now we can submit data!**

---

# The Problem with Forms

- User submits message
- Page refreshes completely
- **No real-time updates**
- Other users don't see new messages
- Poor user experience

**We need something better...**

---

# Enter JavaScript & Websockets

## What are Websockets?

```
Browser ◄──── Persistent Connection ────► Server
        ◄──── Real-time Messages ─────►
```

- **Bidirectional** communication
- **Persistent** connection
- **Real-time** updates
- No page refreshes needed

---

# JavaScript Websocket Basics

```javascript
// Connect to server
const socket = io();

// Send a message
socket.emit('send_message', {
    text: 'Hello world!'
});

// Listen for messages
socket.on('new_message', function(data) {
    console.log('Received:', data);
});
```

---

# Demo 3: First Websocket

```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('echo_message')
def handle_echo_message(data):
    emit('echo_response', data)
```

```javascript
socket.emit('echo_message', {text: 'Hello'});
socket.on('echo_response', function(data) {
    console.log('Echo:', data.text);
});
```

---

# What's Different Now?

- **No page refresh**
- **Instant response**
- JavaScript handles the communication
- Server can send data anytime
- Foundation for real-time apps

---

# Polling vs WebSockets

- Not all servers support websockets
- Firewalls, proxies etc. can block
- **Long polling** as an alternative
- `socket.io` vs `websockets`

---

# Demo 4: Real-time Chat

```python
@socketio.on('send_message')
def handle_send_message(data):
    message = {
        'text': data['text'],
        'timestamp': datetime.now().isoformat()
    }
    messages.append(message)
    # Broadcast to ALL connected users
    emit('new_message', message, broadcast=True)
```

---

# Key JavaScript Patterns

## Sending Data to Server
```javascript
socket.emit('event_name', data);
```

## Receiving Data from Server
```javascript
socket.on('event_name', function(data) {
    // Handle the data
});
```

## Connection Events
```javascript
socket.on('connect', function() {
    console.log('Connected!');
});
```

---

# Demo 5: Enhanced Chat

**New Features:**
- User nicknames
- Join/leave notifications
- Online user list
- Message timestamps

**Key Concept:** Server maintains state about connected users

---

# Demo 6: Advanced Features

**Real-time Interactions:**
- "User is typing" indicators
- Multiple chat rooms
- Private messages

**JavaScript handles complex UI updates**

---

# Typing Indicators Example

```javascript
// Start typing
$('#message-input').on('input', function() {
    socket.emit('typing_start', {room: currentRoom});
});

// Stop typing (with timeout)
setTimeout(() => {
    socket.emit('typing_stop', {room: currentRoom});
}, 1000);
```

---

# Server-Side Room Management

```python
@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    emit('user_joined', {
        'username': session['username']
    }, room=room)
```

---

# Key Takeaways

1. **HTTP** = Request/Response, one-way
2. **Websockets** = Persistent, bidirectional
3. **JavaScript** handles real-time UI updates
4. **Flask-SocketIO** makes server-side easy
5. **Events** are the communication pattern

---

# What You Can Build

- Real-time chat applications
- Live collaborative tools
- Gaming applications
- Live dashboards
- Interactive presentations
- And much more!
