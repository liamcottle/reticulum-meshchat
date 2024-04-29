# Reticulum WebChat

A simple web based [LXMF](https://github.com/markqvist/lxmf) client for [Reticulum](https://github.com/markqvist/Reticulum).

## Features

- Supports sending to and receiving messages from [Sideband](https://github.com/markqvist/Sideband/) and [Nomadnet](https://github.com/markqvist/nomadnet).
- Supports receiving images sent from Sideband.
- Supports receiving file attachments sent from Sideband.

## How does it work?

- A python script (`web.py`) runs a Reticulum instance and a WebSocket server.
- The web page sends and receives lxmf packets encoded in json via the WebSocket.
- Web Browser -> WebSocket -> Python Reticulum -> (configured interfaces) -> (destination)

## How to use it?

You will need to clone the repo, and run `web.py`.

```
git clone https://github.com/liamcottle/reticulum-webchat
cd reticulum-webchat
python web.py
```

> NOTE: You should now be able to access the web interface at http://localhost:8000

## TODO

- [ ] allow passing in a custom port to serve on via cli args
- [ ] allow passing in a custom Reticulum config file via cli args
- [ ] conversations/contacts list ui with unread indicators
- [ ] create/import/export identities in the web ui
- [ ] ui to configure custom name to send in announcement app data
- [ ] ui to view announcements, with names from app data
- [ ] support saving conversation history across page reloads
- [ ] send images from web ui
- [ ] send file attachments from web ui
- [ ] support for multiple (but separated) identities via the same websocket server
  - possibly allow multiple identities to simultaneously send/receive in multiple browser tabs?
