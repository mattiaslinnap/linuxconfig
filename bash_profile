#!/bin/bash

export EDITOR=nano
export PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ "
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

export REPOS='/Users/mattias/repos'
export VENVS='/Users/mattias/venvs'
export DATASETS='/Users/mattias/datasets'
export ANDROID_HOME="$REPOS/android-sdk"
export ANDROID_NDK_HOME="$REPOS/android-ndk"

export WORKON_HOME="$VENVS"
export PATH="/usr/local/bin:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_NDK_HOME:/Applications/Postgres93.app/Contents/MacOS/bin:$PATH"
export PYTHONPATH="$PYTHONPATH:$REPOS/pyshortcuts"
export PSLIMITS_CACHE_DIR="$DATASETS"

if [ -f $REPOS/linuxconfig/bash_functions ]; then
    . $REPOS/linuxconfig/bash_functions
fi

if [ -f $REPOS/linuxconfig/alias ]; then
    . $REPOS/linuxconfig/alias
fi

. /usr/local/bin/virtualenvwrapper.sh

