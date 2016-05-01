#!/bin/bash

if [ $# -ne 2 ]
then
  echo "Usage: $0 <VM password> <retrasmissionFlag>"
  exit 0
fi

source ~/.topology

if [ "$2" == "y" ]; then
  echo "set retransmission flag TRUE" 
  sshpass -p$1 ssh $VMsmall29 "ndn-traffic -i 20 -r NDN_Traffic_Client_KISTI >& ndn-traffic.log"
else
  echo "set retransmission flag FALSE"
  sshpass -p$1 ssh $VMsmall29 "ndn-traffic -i 20 NDN_Traffic_Client_KISTI >& ndn-traffic.log"
fi

