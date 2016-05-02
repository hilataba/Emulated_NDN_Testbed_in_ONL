#!/bin/bash

if [ $# -ne 2 ]
then
  echo "Usage: $0 <VM password> <conf file>"
  exit 0
fi

source ~/.topology

sshpass -p$1 ssh $VMsmall37 "ndn-traffic-server $2 >& ndn-traffic-server.log"
