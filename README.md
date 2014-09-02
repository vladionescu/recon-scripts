recon-scripts
=============

A collection of scripts I wrote to assist in information gathering against targets.

get_links_ips.py
----------------
_Python 2.7_
```
python get_links_ips.py [ -h | -v ] url
```

Scan the source code of a given URL for anything that looks like a link (must begin http/s). Connect to each URL and determine the IP of the server responding to the URL. Outputs results to stdout in format `<ip> <link>\n`.

Use a bash one-liner like the following to get a sorted list of IPs and the number of times each one was hit: `awk '{ print $1 }' out_file | sort | uniq -c | sort -r` where `out_file` is a file with the output from the script.

A smart thing to do would be to modify this script so it can be called recursively on the URLs it finds, with a setting to control how deep it will scan. Enumaration to the max! Beware, this script is already noisy.

sort_nets.py
------------
_Python 2.7_
```
python sort_nets.py [ -h ] infile
```

Given a newline delimited list of IPs (the infile), figure out which network each belongs to and sort IPs by network. Relies on ARIN WHOIS queries returning a CIDR record for this to work. This cannot take into account subnetting done by the organization, it can only find publicly registered IP block boundaries.

You can use the output from get_links_ips.py with this script and, for instance, get a table of the target's various servers linked to from their front page (a lot of organizations serve domain.com/jobs or support.domain.com from different servers).
