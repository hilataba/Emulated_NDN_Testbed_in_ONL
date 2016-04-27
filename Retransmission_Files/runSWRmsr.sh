#!/bin/bash
#run on SWR

source ~/.topology

if (( $# != 1 )); then
  echo "usage: ./runSWRmsr.sh <expName>"
  exit
fi
expName=$1

function clean_up {

	# Perform program exit housekeeping
	echo "closing..."
	sed -i '1i\TO_UIUC' $uiucOut
	sed -i '2i\'$timeval $uiucOut
	sed -i '1i\TO_UM' $umOut
	sed -i '2i\'$timeval $umOut 
	sed -i '1i\TO_CLIENT' $clientOut
	sed -i '2i\'$timeval $clientOut

	exit
}

trap clean_up  SIGHUP SIGINT SIGTERM

# get current timestamp
timeval=$(date +%s)

uiucIf=$(netstat -ie | grep -B1 "192.168.30.2" | head -n1 | awk '{print $1}')
umIf=$(netstat -ie | grep -B1 "192.168.21.2" | head -n1 | awk '{print $1}')
clientIf=$(netstat -ie | grep -B1 "192.168.29.2" | head -n1 | awk '{print $1}')

echo $uiucIf
echo $umIf
echo $clientIf


mkdir '/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'$expName
# set output files
uiucOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_UIUC_$timeval.csv"
umOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_UM_$timeval.csv"
clientOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_CLIENT_$timeval.csv"

echo $uiucOut
echo $umOut
echo $clientOut

# start measurments
~/statmon/statmon $uiucIf tx_packets $uiucOut &
~/statmon/statmon $umIf tx_packets $umOut & 
~/statmon/statmon $clientIf tx_packets $clientOut & 


wait 
clean_up
