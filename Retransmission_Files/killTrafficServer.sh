#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 <VM password>"
  exit 0
fi

source ~/.topology

sshpass -p$1 ssh $VMsmall37 "killall ndn-traffic-server"
sshpass -p$1 scp ${VMsmall37}:~/ndn-traffic-server.log .

