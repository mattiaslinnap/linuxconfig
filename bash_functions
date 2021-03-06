#!/bin/bash
# NOTE: Custom aliases have not been applied yet.

function g()
{
    grep -nHR "$1" * | grep -v Binary | grep -v .svn
}

function resource()
{
    . ~/.bash_profile
}

function newalias()
{
    nano -w -T 4 -E $REPOS/linuxconfig/alias
    resource
}

function newfunc()
{
    nano -w -T 4 -E $REPOS/linuxconfig/bash_functions
    resource
}

