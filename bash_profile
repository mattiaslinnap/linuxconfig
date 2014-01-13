#!/bin/bash

export EDITOR=nano

export REPOS='/Users/mattias/repos'
export VENVS='/Users/mattias/venvs'
export ANDROID_HOME="$REPOS/android-sdk-macosx"
export ANDROID_NDK_HOME="$REPOS/android-ndk-r9b"

export WORKON_HOME="$VENVS"
export PATH="/usr/local/bin:/usr/local/heroku/bin:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_NDK_HOME:$HOME/bin:$PATH"
export PYTHONPATH="$PYTHONPATH:$REPOS/pyshortcuts"
export PSLIMITS_CACHE_DIR="$HOME/datasets"

if [ -f ~/bin/bash_functions ]; then
    . ~/bin/bash_functions
fi

if [ -f ~/bin/alias ]; then
    . ~/bin/alias
fi

. /usr/local/bin/virtualenvwrapper.sh

