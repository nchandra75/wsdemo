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

# On Windows (untested)
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

Note that the `uv.lock` and related files are intentionally left out of this repo so that you can run through all the commands and try it on your own.  The aim of this repo is to encourage experimentation, so if something is broken you can fix it and feel good about it.

```bash
# Start a project
uv init

# For Demo 1 & 2 (basic Flask)
uv add flask

# For Demo 3+ (websockets - install when you reach Demo 3)
uv add flask-socketio

# For the sidebar on websockets
uv add websockets
```

## Running the Demos

Each demo is self-contained and can be run independently. Navigate to the demo directory and run the Flask application.

**WARNING**: The demos here have been set to run on all network interfaces: in general this is insecure as it allows outsiders to connect to a server on your system.  You should either run a firewall, or change this (delete the `host='0.0.0.0'` bit).

### Demo 1: Basic Flask Server
```bash
cd demo1
python app.py
```
Visit: http://localhost:5001

**Purpose:** Review
- Basic Flask application structure
- Routing and templates
- Serving static files

### Demo 2: Forms and Basic Interactivity
```bash
cd demo2
python app.py
```
Visit: http://localhost:5002

**Purpose:** Review
- HTML forms and POST requests
- Form data processing
- Template variables and loops
- **Limitation:** On each form post, a complete new request is being sent to the server that then responds.  This is not much overhead for a small application like this, but is not really *interactive*.

### Sidebar: WebSockets vs SocketIO
Before starting on the websocket demos, check out the `demo-sidebar/` directory to see a side-by-side comparison of raw WebSockets vs Flask-SocketIO. This will help you understand why we use SocketIO as a simpler abstraction.

```bash
cd demo-sidebar
# See the README.md there for instructions
```

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

During the workshop, we will work through the examples, but also have brief interludes talking about background and related knowledge.  If you are only seeing this repo, then it is suggested that you:

1. **Start with Demo 1** - Get familiar with Flask basics
2. **Progress through each demo** - Each builds on the previous
3. **Test each demo** before moving to the next
4. **Experiment** - Try modifying the code to see what happens

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process using the port (replace 5001 with your port)
# (Note: `lsof` probably only works on Linux)
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

## Note on material

This material was prepared for use in the "Fun with Websockets" workshop as part of Paradox 2025 at IIT Madras.  The demo examples were prepared with coding help from [Claude](https://claude.ai/).  Any errors that still exist are intentional and left as exercises to the reader.

None of this code is remotely production ready, and should not be deployed as such on an actual user facing system.  In particular, the code has not been reviewed for security vulnerabilities, and it is quite likely there are simple injection issues that could be exploited without much effort.  The code also displays poorly on mobile platforms - some basic responsive layout has been implemented, but is not well tested, and is known to have issues with scrolling on mobile browsers.  Feel free to fix these and improve the demos.

## Temporary links for the workshop

During the workshop, all the demos can be accessed at the following links.  However, they may go down randomly at any time and are not guaranteed to be available, as there will be tweaking of the code and updating live during the workshop.  These are provided only for the case where someone is not able to access the IITM Intranet ports.

- [Demo 1](https://demo1.wsdemo.dev.nptel.ac.in/)
- [Demo 2](https://demo2.wsdemo.dev.nptel.ac.in/)
- [Demo 3](https://demo3.wsdemo.dev.nptel.ac.in/)
- [Demo 4](https://demo4.wsdemo.dev.nptel.ac.in/)
- [Demo 5](https://demo5.wsdemo.dev.nptel.ac.in/)
- [Demo 6](https://demo6.wsdemo.dev.nptel.ac.in/)
- [Demo 7](https://demo7.wsdemo.dev.nptel.ac.in/)

---

Nitin Chandrachoodan, IIT Madras, 2025