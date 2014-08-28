#!/bin/bash

dira="$1"
dirb="$2"

lista=$(tempfile)
listb=$(tempfile)

cd $dira && find . | sort > $lista
cd $dirb && find . | sort > $listb

diff $lista $listb
rm $lista $listb

