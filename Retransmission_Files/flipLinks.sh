#!/bin/bash

if (( $# != 2 )); then
  echo "usage: ./flipLinks.sh <expName> <vmPass>"
  exit
fi
expName=$1
vmPass=$2

source ~/.topology

swr_path="Emulated_NDN_Testbed_in_ONL/Retransmission_Files/swr_scripts/"
results_path="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data"

# get current timestamp
timeval=$(date +%s)

mkdir $results_path/$expName

echo "setup backroutes and get status for producer: KISTI"
ssh $h36x1 "nfd-status >& $results_path/$expName/nfd-status-kisti-rtr_start "
sshpass -p$2 ssh $VMsmall37 "nfd-status >& nfd-status_kisti_host_start"
ssh $h28x1 "nfd-status >& $results_path/$expName/nfd-status-wustl-rtr_start "

echo "start swr measurements"
ssh $SWR1631 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr1631.sh $expName $timeval &
ssh $SWR1633 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr1633.sh $expName $timeval &

echo "populate VMs with traffic conf files"
./setupTrafficGen.sh $2

echo "start traffic server"
./runTrafficServer.sh $2 NDN_Traffic_Server_KISTI &

echo "start traffic client"
./runTrafficClient.sh $2 NDN_Traffic_Client_KISTI y &

echo "sleep 10"
sleep 10

echo "droping link..."
ssh $SWR1631 sudo $swr_path/drop2.sh 

echo "sleep for 120"
sleep 120

echo "add  link..."
ssh $SWR1631 sudo $swr_path/add2.sh 

echo sleep for 120
sleep 120

echo "stop traffic gen and get statsistics"
sshpass -p$2 ssh $VMsmall29 "killall ndn-traffic" 
sshpass -p$2 scp ${VMsmall29}:~/ndn-traffic.log $results_path/$expName

echo "stop traffic server and get statsistics"
sshpass -p$2 ssh $VMsmall37 "killall ndn-traffic-server" 
sshpass -p$2 scp ${VMsmall37}:~/ndn-traffic-server.log $results_path/$expName



echo "get final stats producer: KISTI"
ssh $h36x1 "nfd-status >& $results_path/$expName/nfd-status-kisti-rtr_final "

sshpass -p$2 ssh $VMsmall37 "nfd-status >& nfd-status_kisti_host_final"
sshpass -p$2 scp ${VMsmall37}:~/nfd-status_kisti_host_start $results_path/$expName/
sshpass -p$2 scp ${VMsmall37}:~/nfd-status_kisti_host_final $results_path/$expName/

echo "get final stats from wustl router"
ssh $h28x1 "nfd-status >& $results_path/$expName/nfd-status-wustl-rtr_final "


echo "getting counters"
ssh $SWR1631 "killall statmon"
ssh $SWR1633 "killall statmon"

echo "done"
