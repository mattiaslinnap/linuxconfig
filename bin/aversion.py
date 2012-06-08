#!/usr/bin/python
"""Searches for packages in apt-cache database, and shows the available version number for each."""

import subprocess
import sys

def stripped_output_lines(args):
	output = subprocess.check_output(args)
	lines = [line.strip() for line in output.split('\n')]
	lines = [line for line in lines if line]
	return lines

def get_version(package):
	for line in stripped_output_lines(['apt-cache', 'show', package]):
		if line.startswith('Version: '):
			return line[9:]
	return '?'

def main(regex):
	for line in stripped_output_lines(['apt-cache', 'search', regex]):
		package, description = line.split(' - ', 1)
		version = get_version(package)
		print '%s %s (%s)' % (package, version, description)

if __name__ == '__main__':
	main(sys.argv[1])

