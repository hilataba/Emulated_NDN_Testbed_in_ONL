#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 <VM password>"
  exit 0
fi

source ~/.topology

sshpass -p$1 ssh $VMsmall29 "killall ndn-traffic"
sshpass -p$1 scp ${VMsmall29}:~/ndn-traffic.log .


