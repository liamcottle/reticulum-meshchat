# MeshChat on a Raspberry Pi

A simple guide to install [MeshChat](https://github.com/liamcottle/reticulum-meshchat) on a Raspberry Pi.

This would allow you to connect an [RNode](https://github.com/markqvist/RNode_Firmware) (such as a Heltec v3) to the Rasbperry Pi via USB, and then access the MeshChat Web UI from another machine on your network.

My intended use case is to run the Pi + RNode combo from my solar-powered shed, and access the MeshChat Web UI via WiFi.

> Note: This has been tested on a Raspberry Pi 4 Model B

## Install Raspberry Pi OS

If you haven't already done so, the first step is to install Raspberry Pi OS onto an sdcard, and then boot up the Pi. Once booted, follow the below commands.

## Update System

```
sudo apt update
sudo apt upgrade
```

## Install System Dependencies

```
sudo apt install git
sudo apt install python3-pip
```

## Install NodeJS v22

```
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg
NODE_MAJOR=22
echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install nodejs
```

## Install MeshChat

```
git clone https://github.com/liamcottle/reticulum-meshchat
cd reticulum-meshchat
pip install -r requirements.txt --break-system-packages
npm install --omit=dev
npm run build-frontend
```

## Run MeshChat

```
python meshchat.py --headless --host 0.0.0.0
```

## Configure Service

Adding a `systemd` service will allow MeshChat to run in the background when you disconnect from the Pi's terminal.

```
sudo nano /etc/systemd/system/reticulum-meshchat.service
```

```
[Unit]
Description=reticulum-meshchat
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=liamcottle
Group=liamcottle
WorkingDirectory=/home/liamcottle/reticulum-meshchat
ExecStart=/usr/bin/env python /home/liamcottle/reticulum-meshchat/meshchat.py --headless --host 0.0.0.0

[Install]
WantedBy=multi-user.target
```

> Note: Make sure to update the usernames in the service file if needed.

```
sudo systemctl enable reticulum-meshchat.service
sudo systemctl start reticulum-meshchat.service
sudo systemctl status reticulum-meshchat.service
```

You should now be able to access MeshChat via your Pi's IP address.

> Note: Don't forget to include the default port `8000`


---

###  STEP-BY-STEP UPGRADE GUIDE
To upgrade your **Meshchat** installation on Raspberry Pi  follow these steps:

####  1. **Stop Meshchat (if running as a service)**

If you set it up with `systemd`, stop the service:

```bash
sudo systemctl stop reticulum-meshchat
```

---

#### ⬇ 2. **Navigate to the Meshchat Directory**

Open a console and go to the folder where Meshchat is installed. Common paths:

```bash
cd ~/reticulum-meshchat
```

or if you cloned it somewhere else, adjust the path accordingly.

---

####  3. **Pull the Latest Code from GitHub**

Ensure you have no local changes, then update:

```bash
git pull origin master
```


---

####  4. **Update Dependencies (if needed)**

Check if the new version requires updated dependencies:

```bash
pip3 install -r requirements.txt --upgrade --break-system-packages
```

---

####  5. **Restart Meshchat**


```bash
sudo systemctl start reticulum-meshchat
```
