#!/bin/bash

if [ $# -ne 3 ]
then
  echo "Usage: $0 <VM password> <conf file> <retrasmissionFlag>"
  exit 0
fi

source ~/.topology

if [ "$3" == "y" ]; then
  echo "set retransmission flag TRUE" 
  sshpass -p$1 ssh $VMsmall29 "ndn-traffic -i 20 -r $2 >& ndn-traffic.log"
else
  echo "set retransmission flag FALSE"
  sshpass -p$1 ssh $VMsmall29 "ndn-traffic -i 20 $2 >& ndn-traffic.log"
fi

