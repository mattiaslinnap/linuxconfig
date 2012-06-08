#!/usr/bin/python
import cPickle
import sys

with open(sys.argv[1]) as f:
	print cPickle.load(f)

