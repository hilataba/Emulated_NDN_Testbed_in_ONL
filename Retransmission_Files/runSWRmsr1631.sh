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
	sed -i '1i\TO_UIUC' $uiucOut
	sed -i '2i\'$timeval $uiucOut
	sed -i '1i\TO_UM' $umOut
	sed -i '2i\'$timeval $umOut 
	sed -i '1i\TO_UA' $uaOut
	sed -i '2i\'$timeval $uaOut 
	sed -i '1i\TO_VERISIGN' $vsOut
	sed -i '2i\'$timeval $vsOut 
	sed -i '1i\TO_URJC'  $urjcOut
	sed -i '2i\'$timeval $urjcOut 
	sed -i '1i\TO_CLIENT' $clientOut
	sed -i '2i\'$timeval $clientOut
	sed -i '1i\FROM_CLIENT' $clientIn
	sed -i '2i\'$timeval $clientIn

	exit
}

trap clean_up  SIGHUP SIGINT SIGTERM

uiucIf=$(netstat -ie | grep -B1 "192.168.30.2" | head -n1 | awk '{print $1}')
umIf=$(netstat -ie | grep -B1 "192.168.21.2" | head -n1 | awk '{print $1}')
uaIf=$(netstat -ie | grep -B1 "192.168.1.2" | head -n1 | awk '{print $1}')
vsIf=$(netstat -ie | grep -B1 "192.168.23.2" | head -n1 | awk '{print $1}')
urjcIf=$(netstat -ie | grep -B1 "192.168.17.1" | head -n1 | awk '{print $1}')
clientIf=$(netstat -ie | grep -B1 "192.168.29.2" | head -n1 | awk '{print $1}')

echo $uiucIf
echo $umIf
echo $uaIf
echo $vsIf
echo $urjcIf
echo $clientIf

mkdir '/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/'$expName
# set output files
uiucOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_UIUC_$timeval.csv"
umOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_UM_$timeval.csv"
uaOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_UA_$timeval.csv"
vsOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_VERISIGN_$timeval.csv"
urjcOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_URJC_$timeval.csv"
clientOut="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/TO_CLIENT_$timeval.csv"
clientIn="/users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/results/raw_data/$expName/FROM_CLIENT_$timeval.csv"

echo $uiucOut
echo $umOut
echo $uaOut
echo $vsOut
echo $urjcOut
echo $clientOut
echo $clientIn

# start measurments
~/statmon/statmon $uiucIf tx_packets $uiucOut &
~/statmon/statmon $umIf tx_packets $umOut & 
~/statmon/statmon $uaIf tx_packets $uaOut & 
~/statmon/statmon $vsIf tx_packets $vsOut & 
~/statmon/statmon $urjcIf tx_packets $urjcOut & 
~/statmon/statmon $clientIf tx_packets $clientOut & 
~/statmon/statmon $clientIf rx_packets $clientIn & 


wait 
clean_up
