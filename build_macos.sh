#!/bin/sh

# build .app for mac
python setup.py bdist_mac

# copy shell script to .app
for DIR in ./build/ReticulumWebChat-*.app/Contents/MacOS; do
  cp ./macos/ReticulumWebChat.sh "$DIR/ReticulumWebChat.sh"
  chmod +x "$DIR/ReticulumWebChat.sh"
done

# todo codesign?
