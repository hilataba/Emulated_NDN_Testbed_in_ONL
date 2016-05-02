#!/bin/bash
CWD=`pwd`

source ~/.topology
source hosts

if (( $# != 2 )); then
  echo "usage: ./configRoutersStrategy.sh <strategyName> <name>"
  exit
fi

if [ "$1" == "n" ]; then
  echo "set ncc" 
  strategy='/localhost/nfd/strategy/ncc'
elif [ "$1" == "n2" ]; then
  echo "set ncc-2"
  strategy='/localhost/nfd/strategy/ncc2'
elif [ "$1" == "n2a" ]; then
  echo "set ncc-2 application"
  strategy='/localhost/nfd/strategy/ncc2a'
elif [ "$1" == "n2n" ]; then
  echo "set ncc-2 network"
  strategy='/localhost/nfd/strategy/ncc2n'
elif [ "$1" == "b2" ]; then
  echo "set best-route 2"
  strategy='ndn:/localhost/nfd/strategy/best-route/%FD%04'
elif [ "$1" == "b3" ]; then
  echo "set best-route 3"
  strategy='ndn:/localhost/nfd/strategy/best-route3/%FD%11'
elif [ "$1" == "b3a" ]; then
  echo "set best-route 3 application"
  strategy='ndn:/localhost/nfd/strategy/best-route3a/%FD%11'
elif [ "$1" == "b3n" ]; then
  echo "set best-route 3 network"
  strategy='ndn:/localhost/nfd/strategy/best-route3n/%FD%11'
else 
  echo "set broadcast"
  strategy='/localhost/nfd/strategy/broadcast'
fi


NAMESPACE="/ndn/kr/re/kisti/host"
NAMESPACE=$2
STRATEGY=$strategy

# ROUTER_HOST_PAIRS contains 'tuples' of
#  router-hosts pair names/prefixes. There can be 
#  duplicate routers but not hosts 
# 
# Host file format is [router name]:[host name]:[prefix advertised]
for s in "${ROUTER_HOST_PAIRS[@]}" 
do
  # split string so we can get : separated parts
  pair_info=(${s//:/ })
  ROUTER=${pair_info[0]}
  #HOST=${pair_info[1]}
  #PREFIX=${pair_info[2]}
  #HOSTIP=${pair_info[5]}
  
  ssh ${!ROUTER} "source ~/.topology ;
		  nfdc set-strategy $NAMESPACE  $STRATEGY "
done
