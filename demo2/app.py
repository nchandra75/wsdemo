"""
Demo 2: Forms and Basic Interactivity
Adds HTML forms and POST request handling to display messages.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory storage for messages
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    username = request.form.get('username', 'Anonymous')
    message = request.form.get('message', '')
    
    if message.strip():  # Only add non-empty messages
        messages.append({
            'username': username,
            'message': message
        })
    
    return redirect(url_for('index'))

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    global messages
    messages = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
