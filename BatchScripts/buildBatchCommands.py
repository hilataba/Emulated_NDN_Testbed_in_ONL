#!/usr/bin/env python
import sys


links={}
nodes={}
nodesSWR={}
nodesPort={}
nodesSubnet={}

def process_nodes():
  #print "process_nodes():"
  f = open('nodes.lint','r')

  line = f.readline()

  #print "line: ", line
  count=0
  while line != '' :
    words = line.split()
    # words[0]: should be comment mark <!--
    # words[1]: should be node name
    # words[2]: should be SWR label
    # words[3]: should be port number
    # words[4]: should be h#x# hostname
    # words[5]: should be IP Address
    # words[6]: should be 24 bit subnet
    # words[7]: should be end of comment mark -->
    #print "Node (words[1]): ", words[1]
    nodes[count]=words[1]
    nodesSWR[words[1]]=words[2]
    nodesPort[words[1]]=words[3]
    nodesSubnet[words[1]]=words[6]
    line = f.readline()
   
def process_links():
  #print "process_links():"
  f = open('links.lint','r')

  line = f.readline()

  #print "line: ", line
  count=0
  while line != '' :
    words = line.split()
    # words[0]: should be comment mark <!--
    # words[1]: should be start node name
    # words[2]: should be end node name
    # words[3]: should be cost
    # words[4]: should be end of comment mark -->
    #print "Link (words[1], words[2], words[3]): ", words[1], words[2], words[3]
    link = (words[1], words[2])
    links[link] = words[3]
    line = f.readline()

def addQueue(swr, port, qid, delay):
    print '  <batchCommand>'
    print '    <!-- ',swr,': Queues -->'
    print '    <component typeName="table">'
    print '      <label>',swr,':port',port,':QueueTable</label>'
    print '    </component>'
    print '    <tableElement>'
    print '      <entry generated="false">'
    print '        <field fieldName="queue_id">',qid,'</field>'
    print '        <field fieldName="rate in Kbps">1000</field>'
    print '        <field fieldName="burst in Kbps">1500</field>'
    print '        <field fieldName="mtu">1500</field>'
    print '        <field fieldName="delay in ms">',delay,'</field>'
    print '        <field fieldName="jitter in ms">0</field>'
    print '        <field fieldName="loss percentage">0</field>'
    print '        <field fieldName="corruption percentage">0</field>'
    print '        <field fieldName="duplicate percentage">0</field>'
    print '      </entry>'
    print '    </tableElement>'
    print '    <command displayLabel="Add Queue" opcode="87" numParams="9">'
    print '      <param plabel="queue_id">'
    print '        <default>',qid,'</default>'
    print '      </param>'
    print '      <param plabel="rate in Kbps">'
    print '        <default>1000</default>'
    print '      </param>'
    print '      <param plabel="burst in Kbps">'
    print '        <default>1500</default>'
    print '      </param>'
    print '      <param plabel="mtu">'
    print '        <default>1500</default>'
    print '      </param>'
    print '      <param plabel="delay in ms">'
    print '        <default>',delay,'</default>'
    print '      </param>'
    print '      <param plabel="jitter in ms">'
    print '        <default>0</default>'
    print '      </param>'
    print '      <param plabel="loss percentage">'
    print '        <default>0</default>'
    print '      </param>'
    print '      <param plabel="corruption percentage">'
    print '        <default>0</default>'
    print '      </param>'
    print '      <param plabel="duplicate percentage">'
    print '        <default>0</default>'
    print '      </param>'
    print '    </command>'
    print '  </batchCommand>'


def addFilter(swr, port, qid, daddr, saddr):
    #print "addFilter: swr port qid daddr saddr"
    #print "addFilter(", swr, port, qid, daddr, saddr, " )"
    print '  <batchCommand>'
    print '    <component typeName=\"table\">'
    print '      <!-- ',swr,': Filters -->'
    print '      <label>',swr,':FilterTable</label>'
    print '    </component>'
    print '    <tableElement>'
    print '      <entry generated="false">'
    print '        <field fieldName="destination_address">',daddr,'</field>'
    print '        <field fieldName="destination_mask">24</field>'
    print '        <field fieldName="source_address">',saddr,'</field>'
    print '        <field fieldName="source_mask">24</field>'
    print '        <field fieldName="protocol">*</field>'
    print '        <field fieldName="destination_port">*</field>'
    print '        <field fieldName="source_port">*</field>'
    print '        <field fieldName="tcp fin">*</field>'
    print '        <field fieldName="tcp syn">*</field>'
    print '        <field fieldName="tcp rst">*</field>'
    print '        <field fieldName="tcp psh">*</field>'
    print '        <field fieldName="tcp ack">*</field>'
    print '        <field fieldName="tcp urg">*</field>'
    print '        <field fieldName="drop">false</field>'
    print '        <field fieldName="output_ports">',port,'</field>'
    print '        <field fieldName="sampling_rate">1</field>'
    print '        <field fieldName="qid">',qid,'</field>'
    print '        <field fieldName="enabled">true</field>'
    print '      </entry>'
    print '    </tableElement>'
    print '    <command displayLabel="AddFilter" opcode="77" numParams="17">'
    print '      <param plabel="destination_address">'
    print '        <default>',daddr,'</default>'
    print '      </param>'
    print '      <param plabel="destination_mask">'
    print '        <default>24</default>'
    print '      </param>'
    print '      <param plabel="source_address">'
    print '        <default>',saddr,'</default>'
    print '      </param>'
    print '      <param plabel="source_mask">'
    print '        <default>24</default>'
    print '      </param>'
    print '      <param plabel="protocol">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="destination_port">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="source_port">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp fin">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp syn">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp rst">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp psh">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp ack">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="tcp urg">'
    print '        <default>*</default>'
    print '      </param>'
    print '      <param plabel="drop">'
    print '        <default>false</default>'
    print '      </param>'
    print '      <param plabel="output_ports">'
    print '        <default>',port,'</default>'
    print '      </param>'
    print '      <param plabel="sampling_rate">'
    print '        <default>1</default>'
    print '      </param>'
    print '      <param plabel="qid">'
    print '        <default>',qid,'</default>'
    print '      </param>'
    print '    </command>'
    print '  </batchCommand>'


if __name__ == '__main__':

    process_links()
    process_nodes()

    qid=10
    print '<?xml version="1.0" ?>'
    print '<batch>'
    for (n1,n2),cost in links.iteritems():
        #print "Link: ", n1, " -- ", n2, " cost: ", cost
        #print "Add queue qid=", qid, " on SWR=", nodesSWR[n1], " port=", nodesPort[n1], " with delay=", cost
        #print "Add filter on SWR=", nodesSWR[n1], " daddr 24 bit subnet = ", nodesSubnet[n1], " saddr 24 bit subnet = ", nodesSubnet[n2], " qid = ", qid, " output port = ", nodesPort[n1]
        addQueue(nodesSWR[n1], nodesPort[n1], qid, cost)
        addFilter(nodesSWR[n1], nodesPort[n1], qid, nodesSubnet[n1], nodesSubnet[n2])
        qid = qid + 1
        #print "Add queue qid=", qid, " on SWR=", nodesSWR[n2], " port=", nodesPort[n2], " with delay=", cost
        #print "Add filter on SWR=", nodesSWR[n2], " daddr 24 bit subnet = ", nodesSubnet[n2], " saddr 24 bit subnet = ", nodesSubnet[n1], " qid = ", qid, " output port = ", nodesPort[n2]
        addQueue(nodesSWR[n2], nodesPort[n2], qid, cost)
        addFilter(nodesSWR[n2], nodesPort[n2], qid, nodesSubnet[n2], nodesSubnet[n1])
        qid = qid + 1
        #print ""

    print '</batch>'


