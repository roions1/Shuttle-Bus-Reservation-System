# TCP Multi-Client Chat Application

A multithreaded TCP chat server and client implemented in Python, allowing multiple users to connect and broadcast messages to each other in real time.

**Author:** Zheqi Ren

## Features
- **Multithreaded TCP server** — spawns one thread per connected client, allowing concurrent handling of multiple users without blocking.
- **Custom length-prefixed protocol** — every message is sent as a fixed 10-byte header (message length) followed by the message body, ensuring reliable message framing over TCP's byte-stream and correctly handling partial reads.
- **Real-time broadcast** — messages sent by one client are relayed by the server to all other connected clients, with the sender's username attached.
- **Thread-safe client registry** — a shared dictionary of connected clients is protected with a lock to avoid race conditions during connect/disconnect events.
- **Graceful disconnect handling** — the server detects dropped connections and cleans up client state automatically.

## Tech Stack
- Python 3
- `socket` (TCP/IP networking)
- `threading` (concurrent client handling)

## How to Run
1. Start the server first:
```bash
   python server.py
```
2. In a separate terminal, start one or more clients:
```bash
   python client.py
```
3. Each client will be prompted to enter a username, then can start sending messages. All messages are broadcast to every other connected client.

## Project Structure
- `server.py` — TCP server: accepts connections, manages clients, broadcasts messages.
- `client.py` — TCP client: connects to the server, sends/receives messages via a background thread.
