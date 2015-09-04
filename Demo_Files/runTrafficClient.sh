#!/bin/bash

source ~/.topology

ssh $VMsmall29 "ndn-traffic -i 20 NDN_Traffic_Client_KISTI >& ndn-traffic.log"
