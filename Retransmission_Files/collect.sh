#!/bin/bash

source ~/.topology

if [ $# -ne 2 ]
then
  echo "usage: ./collect.sh <expPrefix> <vmPass>"
  exit 0
fi

strategies="b3 b2 n2 n"

expName=$1
vmPass=$2
#name="/ndn/distributedDB/producer"
name="/ndn/kr/re/kisti/host"
for s in $strategies
do
	echo $s
	cd ../configuration
	./configRoutersStrategy.sh $s $name
	sleep 3
	cd ../Retransmission_Files
	for i in `seq 1 3`;
	do
		echo "run iteration $i"
		#./distributedAppTest.sh $expName'_'$s'_'$i $vmPass
		./flipLinks.sh $expName'_'$s'_'$i $vmPass
		sleep 10
		ls -l '../configuration/NLSR_OUTPUT/*restart*'
	done
done

