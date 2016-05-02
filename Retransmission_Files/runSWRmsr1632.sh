#!/bin/bash
#run on SWR

source ~/.topology

if (( $# != 2 )); then
  echo "usage: ./runSWRmsr.sh <expName> <timeval>"
  exit
fi
expName=$1
# get current timestamp
#timeval=$(date +%s)
timeval=$2

function clean_up {

	# Perform program exit housekeeping
	echo "closing..."
	sed -i '1i\TO_ORANGE' $orangeOut
	sed -i '2i\'$timeval $orangeOut
	sed -i '1i\FROM_ORANGE' $orangeIn
	sed -i '2i\'$timeval $orangeIn
	exit
}

trap clean_up  SIGHUP SIGINT SIGTERM

orangeIf=$(netstat -ie | grep -B1 "192.168.52.1" | head -n1 | awk '{print $1}')

echo $orangeIf

mkdir '/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'$expName
# set output files
orangeOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_ORANGE_$timeval.csv"
orangeIn="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/FROM_ORANGE_$timeval.csv"

echo $orangeOut
echo $orangeIn

# start measurments
~/statmon/statmon $orangeIf tx_packets $orangeOut &
~/statmon/statmon $orangeIf rx_packets $orangeIn &

wait 
clean_up
