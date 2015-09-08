#!/usr/bin/python

# TODO:
# Send multiple ping requests for each neighbor and then take the average
# Update the return message format

import sys
import os
import subprocess
from neighbors import my_neighbors

interest = sys.argv[1]
site = interest.split("/script")[0]
#print site
n = my_neighbors[site]
#print n

result = ""

for destination in n:
  cmd = "ping -c 1 -n -q " + destination
  #cmd = "ping -i 0.2 -c 5 -n -q " + destination
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  out = out.split("/")
  result += site + ":" + destination + "+" + out[-2] + "&"

print result
