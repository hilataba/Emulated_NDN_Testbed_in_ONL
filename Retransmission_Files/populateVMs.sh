#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 <VM password>"
  exit 0
fi

source ~/.topology

while read vm; do
	echo "${!vm}"
  	sshpass -p$1 scp -r /users/hilata/Emulated_NDN_Testbed_in_ONL/Retransmission_Files/VMBin/usr ${!vm}:~/
	sshpass -p$1 ssh -n ${!vm} "sed -i '1i\PATH=/home/hilata/usr/local/bin:$PATH' .bashrc ; echo $1 | sudo -S /sbin/ldconfig /home/hilata/usr/local/lib/"
	
	echo "done..."
done <vmtargets.txt
