#!/usr/bin/python

# Used for the ipPing.py script
# The my_neighbors dictionary is keyed by the name prefixes
# For ech key, the list of neighboring IP addresses are stored

import sys
import os

my_neighbors = dict()

f = open('linksList', 'r')
for line in f:
  line = line.rstrip()
  key = line.split(" ")
  #print key
  site = key[1]
  ip = key[2]

  if site in my_neighbors:
    my_neighbors[site].append(ip)
  else:
    my_neighbors[site] = []
    my_neighbors[site].append(ip)

#print my_neighbors