#!/bin/bash

if (( $# != 2 )); then
  echo "usage: ./flipLinks.sh <expName> <vmPass>"
  exit
fi
expName=$1
vmPass=$2

#sourctamp
timeval=$(date +%s)

source ~/.topology

swr_path="Emulated_NDN_Testbed_in_ONL/Retransmission_Files/swr_scripts/"
results_path="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data"

mkdir $results_path/$expName

echo "setup backroutes and get status for producer: ORANGE"
ssh $h53x2 "nfdc register -c 1 /ndn/distributedDB/producer/host/ udp4://192.168.52.2:6363 ;
	    nfd-status >& $results_path/$expName/nfd-status-orange-rtr_start "

echo "setup backroutes and get status for producer: KISTI"
ssh $h36x1 "nfdc register -c 1 /ndn/distributedDB/producer/host/ udp4://192.168.37.1:6363 ;
	    nfd-status >& $results_path/$expName/nfd-status-kisti-rtr_start "

ssh $h28x1 "nfd-status >& $results_path/$expName/nfd-status-wustl-rtr_start "

echo "start swr measurements"
ssh $SWR1631 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr1631.sh $expName $timeval &
ssh $SWR1632 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr1632.sh $expName $timeval &
ssh $SWR1633 Emulated_NDN_Testbed_in_ONL/Retransmission_Files/runSWRmsr1633.sh $expName $timeval &

echo "populate VMs with traffic conf files"
./setupTrafficGen.sh $2

sshpass -p$2 ssh $VMsmall37 "nfd-status >& nfd-status_kisti_host_start"
sshpass -p$2 ssh $VMsmall47 "nfd-status >& nfd-status_orange_host_start"

echo "start traffic servers"
sshpass -p$2 ssh $VMsmall37 "ndn-traffic-server NDN_Traffic_Server_Distributed >& ndn-traffic-server.log" &
sshpass -p$2 ssh $VMsmall47 "ndn-traffic-server NDN_Traffic_Server_Distributed >& ndn-traffic-server.log" &

sleep 1
echo "start traffic client"
#./runTrafficClient.sh $2 NDN_Traffic_Client_Distributed y &
echo "set retransmission flag TRUE" 
sshpass -p$2 ssh $VMsmall29 "ndn-traffic -i 20 -r NDN_Traffic_Client_Distributed >& ndn-traffic.log" &


#run for 10 seconds
echo "sleep 10"
sleep 10

echo "kill orange producer"
sshpass -p$2 ssh $VMsmall47 "killall ndn-traffic-server"
sshpass -p$2 scp ${VMsmall47}:~/ndn-traffic-server.log $results_path/$expName/ndn-traffic-server-orange_1

sleep 10

echo "bring orange back again"
sshpass -p$2 ssh $VMsmall47 "ndn-traffic-server NDN_Traffic_Server_Distributed >& ndn-traffic-server.log" &

sleep 5
echo "stop traffic gen and get statsistics"
sshpass -p$2 ssh $VMsmall29 "killall ndn-traffic" 
sshpass -p$2 scp ${VMsmall29}:~/ndn-traffic.log $results_path/$expName

echo "stop traffic server and get statsistics"
sshpass -p$2 ssh $VMsmall37 "killall ndn-traffic-server" 
sshpass -p$2 scp ${VMsmall37}:~/ndn-traffic-server.log $results_path/$expName/ndn-traffic-server-kisti
sshpass -p$2 ssh $VMsmall37 "nfd-status >& nfd-status_kisti_host_final"
sshpass -p$2 scp ${VMsmall37}:~/nfd-status_kisti_host_start $results_path/$expName/
sshpass -p$2 scp ${VMsmall37}:~/nfd-status_kisti_host_final $results_path/$expName/

sshpass -p$2 ssh $VMsmall47 "killall ndn-traffic-server"
sshpass -p$2 scp ${VMsmall47}:~/ndn-traffic-server.log $results_path/$expName/ndn-traffic-server-orange_2
sshpass -p$2 ssh $VMsmall47 "nfd-status >& nfd-status_orange_host_final"
sshpass -p$2 scp ${VMsmall47}:~/nfd-status_orange_host_start $results_path/$expName/
sshpass -p$2 scp ${VMsmall47}:~/nfd-status_orange_host_final $results_path/$expName/


echo "get final stats: ORANGE"
ssh $h53x2 "nfd-status >& $results_path/$expName/nfd-status-orange-rtr_final "

echo "get final stats producer: KISTI"
ssh $h36x1 "nfd-status >& $results_path/$expName/nfd-status-kisti-rtr_final "

echo "get final stats from wustl router"
ssh $h28x1 "nfd-status >& $results_path/$expName/nfd-status-wustl-rtr_final "

echo "getting counters"
ssh $SWR1631 "killall statmon"
ssh $SWR1632 "killall statmon"
ssh $SWR1633 "killall statmon"

echo "done"


