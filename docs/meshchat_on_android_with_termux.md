# MeshChat on Android

It's possible to run on Android from source, using [Termux](https://termux.dev/).

You will need to install a few extra dependencies and make a change to `requirements.txt`.

```
pkg upgrade
pkg install git
pkg install nodejs-lts
pkg install python-pip
pkg install rust
pkg install binutils
pkg install build-essential
```

You should now be able to follow the [how to use it](../README.md#how-to-use-it) instructions above.

Before running `pip install -r requirements.txt`, you will need to comment out the `cx_freeze` dependency. It failed to build on my Android tablet, and is not actually required for running from source.

```
nano requirements.txt
```

Ensure the `cx_freeze` line is updated to `#cx_freeze`

> Note: Building wheel for cryptography may take a while on Android.

Once MeshChat is running via Termux, open your favourite Android web browser, and navigate to http://localhost:8000

> Note: The default `AutoInterface` may not work on your Android device. You will need to configure another interface such as `TCPClientInterface`.
