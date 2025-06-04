"""
Raw WebSocket Echo Server
This shows how to implement a simple echo server using the raw websockets library.
Notice how much manual connection handling is required!
"""

import asyncio
import websockets
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Keep track of connected clients
connected_clients = set()

async def handle_client(websocket, path):
    """Handle a new client connection"""
    # Add client to our set
    connected_clients.add(websocket)
    client_address = websocket.remote_address
    logger.info(f"Client {client_address} connected. Total clients: {len(connected_clients)}")
    
    try:
        # Listen for messages from this client
        async for message in websocket:
            try:
                # Parse the message (assuming JSON)
                data = json.loads(message)
                logger.info(f"Received from {client_address}: {data}")
                
                # Echo the message back
                response = {
                    "type": "echo",
                    "original_message": data.get("message", ""),
                    "timestamp": data.get("timestamp", ""),
                    "from_server": "This is your message echoed back!"
                }
                
                await websocket.send(json.dumps(response))
                
            except json.JSONDecodeError:
                # Handle invalid JSON
                error_response = {
                    "type": "error",
                    "message": "Invalid JSON format"
                }
                await websocket.send(json.dumps(error_response))
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_address} disconnected normally")
    except Exception as e:
        logger.error(f"Error with client {client_address}: {e}")
    finally:
        # Remove client from our set
        connected_clients.discard(websocket)
        logger.info(f"Client {client_address} removed. Total clients: {len(connected_clients)}")

async def main():
    """Start the WebSocket server"""
    logger.info("Starting raw WebSocket server on localhost:8765")
    
    # Start the server
    server = await websockets.serve(handle_client, "localhost", 8765)
    logger.info("Server started! Open websocket_client.html in your browser.")
    
    # Keep the server running
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
