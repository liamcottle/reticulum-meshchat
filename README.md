# Reticulum WebChat

A simple open-source web based [LXMF](https://github.com/markqvist/lxmf) client for [Reticulum](https://github.com/markqvist/Reticulum).

## Features

- Supports sending and receiving messages from [Reticulum WebChat](https://github.com/liamcottle/reticulum-webchat), [Sideband](https://github.com/markqvist/Sideband/) and [Nomadnet](https://github.com/markqvist/nomadnet).
- Supports receiving and saving images and attachments sent from Sideband.
- Supports sending an announce to the network.
- Supports setting a custom display name to send in your announce.
- Supports viewing peers discovered from announces.

## How does it work?

- A python script ([web.py](./web.py)) runs a Reticulum instance and a WebSocket server.
- The web page sends and receives lxmf packets encoded in json via the WebSocket.
- Web Browser -> WebSocket -> Python Reticulum -> (configured interfaces) -> (destination)

## How to use it?

You will need to clone the repo, and run `web.py`.

```
git clone https://github.com/liamcottle/reticulum-webchat
cd reticulum-webchat
pip install -r requirements.txt
python web.py
```

> NOTE: You should now be able to access the web interface at http://localhost:8000

For a full list of command line options, you can run;

```
python web.py --help
```

```
usage: web.py [-h] [--host [HOST]] [--port [PORT]] [--identity-file IDENTITY_FILE] [--identity-base64 IDENTITY_BASE64]

ReticulumWebChat

options:
  -h, --help            show this help message and exit
  --host [HOST]         The address the web server should listen on.
  --port [PORT]         The port the web server should listen on.
  --identity-file IDENTITY_FILE
                        Path to a Reticulum Identity file to use as your LXMF address.
  --identity-base64 IDENTITY_BASE64
                        A base64 encoded Reticulum Identity to use as your LXMF address.
```

## Using an existing Reticulum Identity

By default, a random identity is generated every time you run the script.

This is handy for quickly testing out the web ui, however you may want to use an existing identity when chatting with others.

To generate a new identity, you can use the [rnid](https://reticulum.network/manual/using.html#the-rnid-utility) utility provided by Reticulum.

```
rnid --generate ./new_identity
```

You can then use following to run the web ui with your new identity file;

```
python web.py --identity-file ./new_identity
```

Alternatively, you can provide a base64 encoded private key, like so;

```
python web.py --identity-base64 "GCN6mMhVemdNIK/fw97C1zvU17qjQPFTXRBotVckeGmoOwQIF8VOjXwNNem3CUOJZCQQpJuc/4U94VSsC39Phw=="
```

> NOTE: this is a randomly generated identity for example purposes. Do not use it, it has been leaked!

## TODO

- [ ] make sure web ui can run in offline environment, so host tailwind/vue locally
- [ ] allow passing in a custom Reticulum config file via cli args
- [ ] allow generating identity in python if rnid util is not available
- [ ] send images from web ui
- [ ] send file attachments from web ui
- [ ] support saving conversation history across page reloads, maybe an sqlite database
- [ ] conversations/contacts list ui with unread indicators
- [ ] button to add peer to contacts, and show a tab for contacts
- [ ] allow setting a custom name to show for a contact
- [ ] button to forget peers and contacts
