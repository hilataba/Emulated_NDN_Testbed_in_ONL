#!/bin/bash

source ~/.topology

ssh $VMsmall37 "ndn-traffic -i 20 NDN_Traffic_Server_KISTI >& ndn-traffic-server.log"
