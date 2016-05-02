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
	sed -i '1i\TO_KISTI' $kistiOut
	sed -i '2i\'$timeval $kistiOut
	sed -i '1i\FROM_KISTI' $kistiIn
	sed -i '2i\'$timeval $kistiIn
	exit
}

trap clean_up  SIGHUP SIGINT SIGTERM

kistiIf=$(netstat -ie | grep -B1 "192.168.37.2" | head -n1 | awk '{print $1}')

echo $kistiIf

mkdir '/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'$expName
# set output files
kistiOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_KISTI_$timeval.csv"
kistiIn="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/FROM_KISTI_$timeval.csv"

echo $kistiOut
echo $kistiIn

# start measurments
~/statmon/statmon $kistiIf tx_packets $kistiOut &
~/statmon/statmon $kistiIf rx_packets $kistiIn &

wait 
clean_up
