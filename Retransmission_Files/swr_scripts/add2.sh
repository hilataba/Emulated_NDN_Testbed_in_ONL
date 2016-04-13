#! /bin/bash

#need to know initial priority and mark


echo "delete drop 30 to 28"
ip rule del blackhole fwmark 60 priority 300
echo "delete drop 28 to 30"
ip rule del blackhole fwmark 61 priority 301


echo "add 30 to 28"
ip rule add fwmark 60 table port12Filters priority 300
echo "add 28 to 30"
ip rule add fwmark 61 table port14Filters priority 301
