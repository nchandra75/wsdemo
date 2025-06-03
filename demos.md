# Workshop Demo Progression

This document outlines a suggested series of demonstrations for the "Fun with WebSockets Workshop," building progressively from fundamental web concepts to a complete real-time application.

## Demo 1: Static Flask Website

**Objective:** Introduce the absolute basics of a web server and serving static content.
**Description:** A minimal Flask application that serves a simple HTML page. This demonstrates the request-response cycle without any dynamic content or client-side interactivity.
**Key Concepts:**
*   Flask application setup (`app = Flask(__name__)`)
*   Routing (`@app.route('/')`)
*   Rendering static HTML (`render_template`)
*   HTTP GET requests

## Demo 2: Flask with Client-Side JavaScript Interactivity

**Objective:** Show how JavaScript adds dynamic behavior to a static page, still within the traditional HTTP model.
**Description:** Enhance the previous Flask app by adding client-side JavaScript. This could involve a simple button click that changes text on the page, or a form submission that updates the UI without a full page reload (using basic DOM manipulation).
**Key Concepts:**
*   Integrating JavaScript into HTML
*   DOM manipulation (e.g., `document.getElementById`, `innerText`)
*   Event listeners (e.g., `addEventListener('click', ...)`)
*   Client-side logic vs. server-side logic

## Demo 3: Simple WebSocket Echo Server

**Objective:** Introduce the concept of a persistent, bidirectional connection using WebSockets.
**Description:** A Flask-SocketIO application where the server simply echoes back any message it receives from a client. The client sends a message and displays the echoed response. This highlights the "always-on" connection and immediate feedback.
**Key Concepts:**
*   `Flask-SocketIO` setup
*   Establishing a WebSocket connection (`io()`)
*   Sending messages (`socket.emit()`)
*   Receiving messages (`socket.on()`)
*   Bidirectional communication

## Demo 4: Real-time Multi-user Chat Application

**Objective:** Combine all previous concepts to build a practical, interactive real-time application.
**Description:** A full-featured chat application where multiple users can send and receive messages instantly. This demo will incorporate user joining/leaving, message broadcasting, and potentially typing indicators, as detailed in the `plan.md`.
**Key Concepts:**
*   Broadcasting messages to all connected clients (`emit(..., broadcast=True)`)
*   Handling user connections and disconnections
*   Managing user state on the server (e.g., `connected_users` dictionary)
*   Real-time UI updates for multiple participants
*   Event-driven architecture for real-time events
