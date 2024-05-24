#!/bin/sh

# references for making a macOS .app that runs a shell script
# https://apple.stackexchange.com/a/407885
# https://github.com/Whisky-App/Whisky/issues/107#issuecomment-1592934039
# https://stackoverflow.com/a/71875958
# https://stackoverflow.com/a/5756763

# get path to directory where this script is currently executing from
# we are expecting this to be "ReticulumWebChat.app/Contents/MacOS"
ABSPATH=$(cd "$(dirname "$0")"; pwd -P)

# path to the actual executable that we want to run as a console application (via Terminal)
EXE="$ABSPATH/ReticulumWebChat"

# open actual executable in terminal
# we also provide a custom storage dir within the user home directory
osascript -e "
    tell app \"Terminal\"
        do script \"$EXE --storage-dir ~/.reticulum-webchat; exit $?\"
        activate
    end tell
"
