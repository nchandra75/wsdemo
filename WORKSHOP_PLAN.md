# Fun with Websockets Workshop Plan

**Duration:** 2 hours  
**Target Audience:** Undergraduate students with basic web development background  
**Goal:** Build a real-time chat application using Flask and websockets

## Workshop Structure

### Phase 1: Foundation (20 minutes)
- **Demo 1** (10 min): Basic Flask Server
  - Simple Flask app with static HTML
  - Basic routing and Jinja2 templates
  - Students run their first server
  
- **Demo 2** (10 min): Forms and Basic Interactivity
  - HTML forms for message input
  - POST requests to submit messages
  - Display messages (requires page refresh)

### Phase 2: Websockets Introduction (30 minutes)
- **Demo 3** (15 min): First Websocket Connection
  - Add Flask-SocketIO
  - Basic client-server websocket connection
  - Echo functionality (send message, get it back)
  
- **Demo 4** (15 min): Real-time Chat Foundation
  - Multiple users can connect
  - Messages broadcast to all users
  - Basic chat room functionality

### Phase 3: Interactive Chat Features (45 minutes)
- **Demo 5** (20 min): Enhanced Chat
  - User nicknames/usernames
  - Join/leave notifications
  - Message timestamps
  - Online user list
  
- **Demo 6** (25 min): Advanced Features
  - "User is typing" indicators
  - Private messages/whispers
  - Multiple chat rooms/channels

### Phase 4: Game-like Features (20 minutes)
- **Demo 7** (20 min): Interactive Elements
  - Real-time voting/polling
  - Emoji reactions
  - Simple collaborative features

### Wrap-up (5 minutes)
- Q&A and discussion of next steps

## Technical Requirements

### Dependencies
- Python 3.7+
- Flask
- Flask-SocketIO
- Basic HTML/CSS/JavaScript knowledge

### Learning Objectives
1. Understand the difference between HTTP and websocket communication
2. Learn to set up Flask-SocketIO
3. Implement real-time bidirectional communication
4. Build interactive web applications
5. Handle multiple concurrent users

## Demo Progression Strategy

Each demo builds on the previous one, with complete working code at each stage. Students can:
- Follow along step by step
- Jump to any demo if they fall behind
- See immediate results at each stage
- Experiment with modifications

## Instructor Notes

- Have students test each demo before moving to the next
- Encourage experimentation and questions
- Provide troubleshooting help for common issues
- Show browser developer tools for websocket debugging
