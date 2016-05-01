#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 <VM password>"
  exit 0
fi

source ~/.topology

while read vm; do
	echo "${!vm}"
	#sshpass -p$1 scp -r /users/hilata/nfd/usr ${!vm}:~/
	sshpass -p$1 scp -r /users/hilata/nfd/ndn-cxx-hila/ ${!vm}:~/
  	sshpass -p$1 scp -r /users/hilata/nfd/NFD-hila/ ${!vm}:~/
  	sshpass -p$1 scp -r /users/hilata/nfd/ndn-traffic-gen-hila ${!vm}:~/
  	sshpass -p$1 scp /users/hilata/nfd/conf ${!vm}:~/
	sshpass -p$1 ssh -n ${!vm} "./conf ; sed -i '1i\PATH=/home/hilata/usr/local/bin:$PATH' .bashrci ; sudo /sbin/ldconfig /home/hilata/usr/local/lib/"
	
	echo "done..."
done <vmtargets.txt
