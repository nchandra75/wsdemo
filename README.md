# Fun with Websockets Workshop

A hands-on workshop for undergraduate students to learn websockets through building a real-time chat application with Flask.

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- Basic knowledge of HTML, CSS, and Python

## Setup

### 1. Install uv (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
# For Demo 1 & 2 (basic Flask)
uv add flask

# For Demo 3+ (websockets - install when you reach Demo 3)
uv add flask-socketio
```

## Running the Demos

Each demo is self-contained and can be run independently. Navigate to the demo directory and run the Flask application.

### Demo 1: Basic Flask Server
```bash
cd demo1
python app.py
```
Visit: http://localhost:5001

**What you'll learn:**
- Basic Flask application structure
- Routing and templates
- Serving static files

### Demo 2: Forms and Basic Interactivity
```bash
cd demo2
python app.py
```
Visit: http://localhost:5002

**What you'll learn:**
- HTML forms and POST requests
- Form data processing
- Template variables and loops
- **Limitation:** Page refresh required to see new messages

### Demo 3: First Websocket Connection
```bash
cd demo3
python app.py
```
Visit: http://localhost:5003

**What you'll learn:**
- Introduction to Flask-SocketIO
- Basic websocket connection
- Real-time communication (echo functionality)

### Demo 4: Real-time Chat Foundation
```bash
cd demo4
python app.py
```
Visit: http://localhost:5004

**What you'll learn:**
- Broadcasting messages to all users
- Multiple concurrent connections
- Basic chat room functionality

### Demo 5: Enhanced Chat
```bash
cd demo5
python app.py
```
Visit: http://localhost:5005

**What you'll learn:**
- User nicknames and join/leave notifications
- Message timestamps
- Online user list

### Demo 6: Advanced Features
```bash
cd demo6
python app.py
```
Visit: http://localhost:5006

**What you'll learn:**
- "User is typing" indicators
- Private messages/whispers
- Multiple chat rooms

### Demo 7: Interactive Elements
```bash
cd demo7
python app.py
```
Visit: http://localhost:5007

**What you'll learn:**
- Real-time voting/polling
- Emoji reactions
- Collaborative features

## Workshop Flow

1. **Start with Demo 1** - Get familiar with Flask basics
2. **Progress through each demo** - Each builds on the previous
3. **Test each demo** before moving to the next
4. **Experiment** - Try modifying the code to see what happens
5. **Ask questions** - The instructor is there to help!

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process using the port (replace 5001 with your port)
lsof -ti:5001 | xargs kill -9
```

**Dependencies not found:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Reinstall dependencies
uv add flask flask-socketio
```

**Browser not connecting to websockets:**
- Check browser developer tools (F12) for errors
- Ensure you're using the correct port
- Try refreshing the page

### Testing Multiple Users

To test chat functionality with multiple users:
1. Open multiple browser tabs/windows
2. Or use different browsers
3. Or use incognito/private browsing mode
4. All pointing to the same localhost URL

## Next Steps

After completing the workshop, consider exploring:
- Database integration (SQLite, PostgreSQL)
- User authentication and sessions
- Deployment to cloud platforms
- More advanced websocket features
- Integration with frontend frameworks (React, Vue)

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [WebSocket Protocol](https://tools.ietf.org/html/rfc6455)
- [uv Documentation](https://docs.astral.sh/uv/)
