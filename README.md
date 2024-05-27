<p align="center">
<a href="https://github.com/liamcottle/reticulum-webchat"><img src="./logo/logo-chat-bubble.png" width="150"></a>
</p>

<h2 align="center">Reticulum WebChat</h2>

<p align="center">
<a href="https://discord.gg/APQSQZNV7t"><img src="https://img.shields.io/badge/Discord-Liam%20Cottle's%20Discord-%237289DA?style=flat&logo=discord" alt="discord"/></a>
<a href="https://twitter.com/liamcottle"><img src="https://img.shields.io/badge/Twitter-@liamcottle-%231DA1F2?style=flat&logo=twitter" alt="twitter"/></a>
<br/>
<a href="https://ko-fi.com/liamcottle"><img src="https://img.shields.io/badge/Donate%20a%20Coffee-liamcottle-yellow?style=flat&logo=buy-me-a-coffee" alt="donate on ko-fi"/></a>
<a href="./donate.md"><img src="https://img.shields.io/badge/Donate%20Bitcoin-3FPBfiEwioWHFix3kZqe5bdU9F5o8mG8dh-%23FF9900?style=flat&logo=bitcoin" alt="donate bitcoin"/></a>
</p>

## What is Reticulum WebChat?

A simple mesh network communications app powered by the [Reticulum Network](https://github.com/markqvist/Reticulum).

- It can communicate with any other [LXMF](https://github.com/markqvist/lxmf) client.
- It can browse micron pages and download files from [Nomad Network](https://github.com/markqvist/nomadnet) nodes.
- It can send and receive messages, files and audio calls with peers;
  - Over your local network through Ethernet and WiFi, completely automatically.
  - Over the internet by connecting through a server hosted by yourself or the community.
  - Over low-powered, license-free, ISM band LoRa Radio, with an [RNode](https://github.com/markqvist/RNode_Firmware).
  - ...and via any other interface supported by the Reticulum Network Stack.
  

<img src="./screenshots/screenshot.png">

## Features

- Supports sending and receiving messages between [Reticulum WebChat](https://github.com/liamcottle/reticulum-webchat), [Sideband](https://github.com/markqvist/Sideband/) and [Nomadnet](https://github.com/markqvist/nomadnet).
- Supports receiving and saving images and attachments sent from Sideband.
- Supports sending images and file attachments.
- Supports saving inbound and outbound messages to a local database.
- Supports sending an announce to the network.
- Supports setting a custom display name to send in your announce.
- Supports viewing and searching peers discovered from announces.

## Beta Features

- Support for Audio Calls to other [Reticulum WebChat](https://github.com/liamcottle/reticulum-webchat) users.
  - Audio is encoded with [codec2](https://github.com/drowe67/codec2) to support low bandwidth links.
  - Using a microphone requires using the web ui over localhost or https, due to [AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet) secure context.
  - I have tested two-way audio calls over LoRa with a single hop. It works well when a reasonable bitrate is configured on the RNode.
- Support for browsing pages, and downloading files hosted on Nomad Network Nodes.

> NOTE: micron format parsing is still in development, some pages may not render or work correctly at all.

## Download

You can download the latest version for Windows and Mac from the [releases](https://github.com/liamcottle/reticulum-webchat/releases) page.

Alternatively, you can download the source and run it manually from a command line.

See the ["How to use it?"](#how-to-use-it) section below on how to do this.

## How does it work?

- A python script ([web.py](./web.py)) runs a Reticulum instance and a WebSocket server.
- The web page sends and receives LXMF packets encoded in json via the WebSocket.
- Web Browser -> WebSocket -> Python Reticulum -> (configured interfaces) -> (destination)
- LXMF messages sent and received are saved to a local SQLite database.

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
usage: web.py [-h] [--host [HOST]] [--port [PORT]] [--headless] [--identity-file IDENTITY_FILE] [--identity-base64 IDENTITY_BASE64] [--generate-identity-file GENERATE_IDENTITY_FILE] [--generate-identity-base64]
              [--reticulum-config-dir RETICULUM_CONFIG_DIR] [--storage-dir STORAGE_DIR]

ReticulumWebChat

options:
  -h, --help            show this help message and exit
  --host [HOST]         The address the web server should listen on.
  --port [PORT]         The port the web server should listen on.
  --headless            Web browser will not automatically launch when this flag is passed.
  --identity-file IDENTITY_FILE
                        Path to a Reticulum Identity file to use as your LXMF address.
  --identity-base64 IDENTITY_BASE64
                        A base64 encoded Reticulum Identity to use as your LXMF address.
  --generate-identity-file GENERATE_IDENTITY_FILE
                        Generates and saves a new Reticulum Identity to the provided file path and then exits.
  --generate-identity-base64
                        Outputs a randomly generated Reticulum Identity as base64 and then exits.
  --reticulum-config-dir RETICULUM_CONFIG_DIR
                        Path to a Reticulum config directory for the RNS stack to use (e.g: ~/.reticulum)
  --storage-dir STORAGE_DIR
                        Path to a directory for storing databases and config files (default: ./storage)
```

## Using an existing Reticulum Identity

The first time you run this application, a new Reticulum identity is generated and saved to `storage/identity`.

If you want to use an existing identity;

- You can overwrite `storage/identity` with another identity file.
- Or, you can pass in a custom identity file path as a command line argument.

To use a custom identity file, provide the `--identity-file` argument followed by the path to your custom identity file.

```
python web.py --identity-file ./custom_identity_file
```

If you would like to generate a new identity, you can use the [rnid](https://reticulum.network/manual/using.html#the-rnid-utility) utility provided by Reticulum.

```
rnid --generate ./new_identity_file
```

If you don't have access to the `rnid` command, you can use the following:

```
python web.py --generate-identity-file ./new_identity_file
```

Alternatively, you can provide a base64 encoded private key, like so;

```
python web.py --identity-base64 "GCN6mMhVemdNIK/fw97C1zvU17qjQPFTXRBotVckeGmoOwQIF8VOjXwNNem3CUOJZCQQpJuc/4U94VSsC39Phw=="
```

> NOTE: this is a randomly generated identity for example purposes. Do not use it, it has been leaked!

## Build Electron Application

Reticulum WebChat can be run from source via a command line, as explained above, or as a standalone application.

To run as a standalone application, we need to compile the python script and dependencies to an executable with [cxfreeze](https://github.com/marcelotduarte/cx_Freeze) and then build an [Electron](https://www.electronjs.org/) app which includes a bundled browser that can interact with the compiled python executable.

This allows for the entire application to be run by double clicking a single file without the need for a user to manually install python, nor run any commands in a command line application.

To build a `.exe` when running on Windows or a `.dmg` when running on a Mac, run the following;

```
pip install -r requirements.txt
npm install
npm run dist
```

> Note: cxfreeze only supports building an executable for the current platform. You will need a Mac to build for Mac, and a Windows PC to build for Windows.

Once completed, you should have a `.exe` or a `.dmg` in the `dist` folder.

## TODO

- [ ] auto build and release windows and macos binaries via github actions
- [ ] conversations/contacts list ui with unread indicators
- [ ] button to add peer to contacts, and show a tab for contacts, separate from peers list
- [ ] allow setting a custom name to show for a contact
- [ ] button to forget peers and contacts
- [ ] optimise ui to work nicely on a mobile device, such as Android/iOS
- [ ] support for managing Reticulum config/interfaces via the web ui
- [ ] support for micron input fields, to allow interacting with pages like Retipedia

## License

MIT
