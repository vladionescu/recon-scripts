#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import re

'''
Usage: script.py [ -h | -v ] url

Given a valid URL (must include protocol) connect to it and parse the returned content for http/s links.

Connect to each link in order and determine the IP address of the connected server.

Prints results in the following format:
<ip> <url>
'''
# TODO:
# select user agent - option to randomize from list
# group IPs on the same network

def usage():
	print >> sys.stderr, 'Usage:', sys.argv[0], '[ -h | -v ]', 'url'
	exit(2)

if len(sys.argv) == 3 or len(sys.argv) == 2:
	if len(sys.argv) == 3 and sys.argv[1] == '-v':
		verbose = True
		initurl = sys.argv[2]
	elif sys.argv[1] != '-h':
		verbose = False
		initurl = sys.argv[1]
	else:
		usage()
else:
	usage()

if verbose:
	print "- Trying", initurl

# get the html
page = urllib2.urlopen(initurl).read()

# find all links in the source code
links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)

# trust only links with a . somewhere in there
# this prevents situations like random http://www in the code
# which gets your local search domain appended when resolved
validlinks = []

for link in links:
	if re.search('\.', link):
		validlinks.append(link)

if verbose:
	print "-", len(validlinks), "links found on", initurl

# get the IP associated with each link
for link in validlinks:
	if verbose:
		print '- Connecting to', link

	try:
		q = urllib2.urlopen(link)
		print q.fp._sock.fp._sock.getpeername()[0] + ' ' + link
	except:
		pass
