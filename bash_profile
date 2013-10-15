#!/bin/bash

export EDITOR=nano

export REPOS='/Users/mattias/repos'
export VENVS='/Users/mattias/venvs'

export WORKON_HOME="$VENVS"
export PATH="/usr/local/bin:/usr/local/heroku/bin:$HOME/bin:$PATH"
export PYTHONPATH="$PYTHONPATH:$REPOS/pyshortcuts"

if [ -f ~/bin/bash_functions ]; then
    . ~/bin/bash_functions
fi

if [ -f ~/bin/alias ]; then
    . ~/bin/alias
fi

. /usr/local/bin/virtualenvwrapper.sh

