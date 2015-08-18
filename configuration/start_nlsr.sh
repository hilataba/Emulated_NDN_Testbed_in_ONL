#!/bin/bash

NAME=$1
while true
do
  echo "starting nlsr >$NAME<"
  nlsr -f ./NLSR_CONF/$NAME.conf > ./NLSR_OUTPUT/$NAME.OUTPUT 2>&1 
  echo "nlsr died, sleep 10 and restart" >> ./NLSR_OUTPUT/$NAME.NLSR.restart.log 
  sleep 10
done
