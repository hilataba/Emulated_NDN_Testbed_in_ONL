#!/bin/bash

if (( $# != 1 )); then
  echo "usage: ./flipLinks.sh <expName>"
  exit
fi
expName=$1

source ~/.topology

swr_path="Emulated_NDN_Testbed_in_ONL/Retransmission_Files/swr_scripts/"

echo "start swr measurements"
ssh $SWR1631 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr.sh $expName &

echo "sleep 4"
sleep 4

ssh $SWR1631 sudo $swr_path/drop2.sh 

sleep 120

ssh $SWR1631 sudo $swr_path/add2.sh

sleep 120

ssh $SWR1631 "killall statmon"

