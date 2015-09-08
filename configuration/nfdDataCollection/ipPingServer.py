#!/usr/bin/python

import time
import BaseHTTPServer

import process_topology as topo

import os
import time
import sys
#import html
#from terminaltables import AsciiTable

# Each
HOST_NAME = '192.168.21.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80

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
    key = topo.site_prefix2site[comps[1]] + " --> " + topo.ip_prefix2site[comps[2]]
    link_id = comps[0]
    key_id[key] = link_id
    id_key[int(link_id)] = key
    id_rtt.append(0)

def dump_rtt():
  processed = dict()
  for link_id in range(1, len(id_rtt)):
    key = id_key[link_id]
    if key not in processed:
      one_line = []
      one_line.append("{:<3}".format(str(link_id)))
      one_line.append("{:<20}".format(id_key[link_id].upper()))
      one_line.append("{:<10}".format(str(id_rtt[link_id])))
			
      r_key = key.split(" --> ")[1] + " --> " + key.split(" --> ")[0]
      r_id = int(key_id[r_key])
      one_line.append("{:<3}".format(str(r_id)))
      one_line.append("{:<20}".format(id_key[r_id].upper()))
      one_line.append("{:<10}".format(str(id_rtt[r_id])))

      processed[key] = 1
      processed[r_key] = 1

      print one_line
      #table_data.append(one_line)
      #table = AsciiTable(table_data)
  #print table.table

def dump_rtt_html():
  table_code = ""
  table_code += '<table>\n'
  for link_id in range(1, len(id_rtt)):
    table_code += '<tr>\n'
    table_code += '<td>'+str(link_id)+'</td><td>'+id_key[link_id]+'</td><td>'+str(id_rtt[link_id])+'</td>'+"\n"
    table_code += '</tr>\n'
  table_code += '</table>\n'

  return table_code

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    """Respond to a GET request."""
    if "/ipPing/" in s.path:
      msg = s.path.split("/ipPing/")[1]
      comps = msg.split("&")
      comps.pop(-1) # remove the last element

      for comp in comps:
        key = comp.split("+")[0]
        if key[0] != '/':
          key = "/" + key
        rtt = comp.split("+")[1]

        key_0 = key.split(":")[0]
        key_1 = key.split(":")[1]

        key_0 = topo.site_prefix2site[key_0]
        key_1 = topo.ip_prefix2site[key_1]

        key = key_0 + " --> " + key_1
        link_id = key_id[key]
        id_rtt[int(link_id)] = rtt

      global update
      update = update + 1
      if update > 100:
        os.system('clear')
        dump_rtt()
        update = 0

    if "/get_ip_rtt.html" == s.path:
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write("<html><head><title>IP RTT.</title></head>")
      # s.wfile.write("<body><p>This is a test.</p>")
      # If someone went to "http://something.somewhere.net/foo/bar/",
      # then s.path equals "/foo/bar/".
      # s.wfile.write("<p>You accessed path: %s</p>" % s.path)
      s.wfile.write(dump_rtt_html())
      s.wfile.write("</body></html>")

if __name__ == '__main__':

  populate_id_rtt_table()

  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

