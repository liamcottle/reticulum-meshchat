# MeshChat on Docker

A docker image is automatically built by GitHub actions, and can be downloaded from the GitHub container registry.

```
docker pull ghcr.io/liamcottle/reticulum-meshchat:latest
```

Additionally, an example [docker-compose.yml](../docker-compose.yml) is available.

The example automatically generates a new reticulum config file in the `meshchat-config` volume. The MeshChat database is also stored in this volume.

Alternatively on a linux box the included [meshchat_docker_mgr.sh](meshchat_docker_mgr.sh) script can be leveraged to automate some common tasks for the container.

Simply run the script with a sudoer user and it will prompt to perform various actions to help create, backup, or restore the container. Backup files should be placed in the same directory as the script, and if it is desired to import a sample reticulum config simply place a file "config" into the same directory as the script before running it.
