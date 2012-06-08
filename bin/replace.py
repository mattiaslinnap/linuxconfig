#!/usr/bin/python

from itertools import islice, izip
import optparse
import re
import sys

def input(opts):
	if opts.file:
		with open(opts.file) as f:
			return f.read()
	else:
		return sys.stdin.read()

def output(opts, data):
	if opts.file:
		with open(opts.file, 'w') as f:
			print >> f, data,  # No endline added, unless it is already part of data
	else:
		print data,

def main(opts, args):
	data = input(opts)
	searches = islice(args, 0, None, 2)
	replaces = islice(args, 1, None, 2)
	for search, replace in izip(searches, replaces):
		data = data.replace(search, replace)
	output(opts, data)


if __name__ == '__main__':
	oparser = optparse.OptionParser()
	oparser.add_option('-f', '--file', dest='file', help='Read and write file instad of stdin/stdout. Useful for replacing in-place.')
	opts, args = oparser.parse_args()
	
	if len(args) < 1:
		oparser.error('Argument pairs of search and replacement strings are required.')
	elif len(args) % 2 == 1:
		oparser.error('Arguments must be in pairs: search and replacement string.')
	else:
		main(opts, args)

