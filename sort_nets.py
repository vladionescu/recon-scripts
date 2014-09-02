#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import struct
import socket
import subprocess

'''
Usage: script.py [ -h ] infile

Given a file (newline delimited list of IPs), run a WHOIS on each IP and get its network's CIDR mask.

Group all IPs in the same network together. Print results to stdout.
'''

def in_net(ip, net):
    "Is an address in a network"
    ipaddr = struct.unpack('>L',socket.inet_aton(ip))[0]
    netaddr,bits = net.split('/')
    netmask = struct.unpack('>L',socket.inet_aton(netaddr))[0]
    return (ipaddr & (4294967295<<(32-int(bits)))) == netmask

# check calling arguments
ips = ''
if len(sys.argv) > 1 and sys.argv[1] and sys.argv[1] != '-h':
	# if it looks like we weren't given -h, read IPs from file
	ips = open(sys.argv[1], 'r').read()
else:
	print >> sys.stderr, 'Usage:', sys.argv[0], '[ -h ]', 'infile'
	exit(2)

# detect if IPs are in the same network
nets = {}
for item in ips.split():
	ip = item.strip()

	# check if this IP is in any networks we already know about
	if len(nets) > 0:
		for net in nets:
			if in_net(ip, net):
				# if it is in a network we know
				# add it to that network's list of IPs
				nets[net].append(ip)

				# go to the next IP address
				break
		else:
			# if it isn't in a network we know
			# learn its network via WHOIS
			newnet = subprocess.Popen("whois " + ip + " | grep 'CIDR' | awk '{ print $2 }'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
			
			# if the WHOIS query returned a network, add it
			if newnet:
				nets[newnet.strip()] = [ip]
	else:
		# if we don't know about any networks
		# learn its network via WHOIS
		newnet = subprocess.Popen("whois " + ip + " | grep 'CIDR' | awk '{ print $2 }'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
		
		# if the WHOIS query returned a network, add it
		if newnet:
			nets[newnet.strip()] = [ip]

# output the IPs grouped by network
for net in nets:
	print net
	print '----------------'
	for ip in nets[net]:
		print ip

	print ''
