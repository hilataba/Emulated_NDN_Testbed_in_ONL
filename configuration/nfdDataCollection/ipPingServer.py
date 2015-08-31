#!/usr/bin/python

import time
import BaseHTTPServer

import os
import time
import sys
from terminaltables import AsciiTable

# Each

HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

#key format: /name/prefix-192.168.1.1 (neighbor IP address)
key_id = dict()
id_key = dict()
id_rtt = [0]
table_data = [["Link ID", "Prefix-IP Pair", "RTT (ms)"]]

update = 0
last_update = 0

def populate_id_rtt_table():
  f = open('linksList', 'r')
  for line in f:
    line = line.rstrip()
    comps = line.split(" ")
    key = comps[1] + "-" + comps[2]
    link_id = comps[0]
    key_id[key] = link_id
    id_key[int(link_id)] = key
    id_rtt.append(0)

def dump_rtt():
  for link_id in range(1, len(id_rtt)):
    one_line = []
    one_line.append(str(link_id))
    one_line.append(id_key[link_id])
    one_line.append(str(id_rtt[link_id]))
    table_data.append(one_line)
    table = AsciiTable(table_data)
  print table.table

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    """Respond to a GET request."""
    print s.path

    # global update
    # update = update + 1
    # if update > 100:
    #   os.system('clear')
    #   dump_rtt()
    #   update = 0

    # s.send_response(404)
    # s.send_header("Content-type", "text/html")
    # s.end_headers()
    # s.wfile.write("<html><head><title>Title goes here.</title></head>")
    # s.wfile.write("<body><p>This is a test.</p>")
    # # If someone went to "http://something.somewhere.net/foo/bar/",
    # # then s.path equals "/foo/bar/".
    # s.wfile.write("<p>You accessed path: %s</p>" % s.path)
    # s.wfile.write("</body></html>")

if __name__ == '__main__':

  populate_id_rtt_table()
  # dump_rtt()

  # exit()

  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
