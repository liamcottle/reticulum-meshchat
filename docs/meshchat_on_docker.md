# MeshChat on Docker

A docker image is automatically built by GitHub actions, and can be downloaded from the GitHub container registry.

```
docker pull ghcr.io/liamcottle/reticulum-meshchat:master
```

Additionally, an example [docker-compose.yml](../docker-compose.yml) is available.

The example automatically generates a new reticulum config file in the `meshchat-config` volume. The MeshChat database is also stored in this volume.
