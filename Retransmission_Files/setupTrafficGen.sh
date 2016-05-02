#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $0 <VM password>"
  exit 0
fi

source ~/.topology

while read vm; do
	echo "${!vm}"
	sshpass -p$1 scp NDN_Traffic_Client_Distributed NDN_Traffic_Server_Distributed NDN_Traffic_Client_KISTI NDN_Traffic_Server_KISTI ${!vm}:~/
done <vmtargets.txt
