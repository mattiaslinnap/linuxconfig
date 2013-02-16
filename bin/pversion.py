#!/usr/bin/python
"""Searches for packages in PyPI web index, and shows the available version number for each."""

import bs4
import cPickle
import datetime
import requests
import sys


PYPI_URL = 'http://pypi.python.org/pypi?%3Aaction=index'
CACHE_FILE = '/home/ml421/.pversion.cache'


def parse_packages(html):
	soup = bs4.BeautifulSoup(html)
	table = soup.find('table', 'list')
	for tr in table.findAll('tr'):
		tds = tr.findAll('td')
		if len(tds) == 2:
			url = tds[0].a['href'].split('/')
			package = str(url[-2])
			version = str(url[-1])
			description = unicode(tds[1].string)
			yield package, version, description

def get_new_packages():
	req = requests.get(PYPI_URL)
	assert req.status_code == 200
	return list(parse_packages(req.content))

def get_cached_packages():
	try:
		with open(CACHE_FILE) as f:
			timestamp, packages = cPickle.load(f)
		if datetime.datetime.utcnow() - timestamp > datetime.timedelta(days=1):
			raise IOError('Too old')
		return packages
	except IOError:
		packages = get_new_packages()
		with open(CACHE_FILE, 'w') as f:
			cPickle.dump((datetime.datetime.utcnow(), packages), f, -1)
		return packages

def print_package(package, version, description):
	print '%s %s (%s)' % (package, version, ' '.join(description.split()))

def main(regex):
	regex = regex.lower()
	packages = get_cached_packages()
	for package, version, description in packages:
		if regex in package.lower():
			print_package(package, version, description)

	print
	print 'Exact matches:'
	for package, version, description in packages:
		if regex == package.lower():
			print_package(package, version, description)

if __name__ == '__main__':
	main(sys.argv[1])

