#!/bin/sh

# ensure macos/ReticulumWebChat.sh is executable before the cxfreeze copies it inside the .app
chmod +x macos/ReticulumWebChat.sh

# build macos .app and put in .dmg
python setup.py bdist_dmg

# todo codesign?
