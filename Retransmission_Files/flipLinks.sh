#!/bin/bash

if (( $# != 2 )); then
  echo "usage: ./flipLinks.sh <expName> <vmPass>"
  exit
fi
expName=$1
vmPass=$2

source ~/.topology

swr_path="Emulated_NDN_Testbed_in_ONL/Retransmission_Files/swr_scripts/"
results_path="results/raw_data"

echo "start swr measurements"
ssh $SWR1631 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr.sh $expName &

echo "populate VMs with traffic conf files"
./setupTrafficGen.sh $2

echo "start traffic server"
./runTrafficServer.sh $2 &

echo "start traffic client"
./runTrafficClient.sh $2 &

echo "sleep 10"
sleep 10

echo "droping link..."
ssh $SWR1631 sudo $swr_path/drop2.sh 

echo "sleep for 120"
sleep 120

echo "getting counters"
ssh $SWR1631 "killall statmon"

echo "stop traffic gen and get statsistics"
sshpass -p$2 ssh $VMsmall29 "killall ndn-traffic" 
sshpass -p$2 scp ${VMsmall29}:~/ndn-traffic.log $results_path/$expName

echo "stop traffic server and get statsistics"
sshpass -p$2 ssh $VMsmall37 "killall ndn-traffic-server" 
sshpass -p$2 scp ${VMsmall37}:~/ndn-traffic-server.log $results_path/$expName

echo "done"
