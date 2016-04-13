#! /bin/bash

#need to know initial priority and mark


echo "delete drop 30 to 28"
ip rule del blackhole fwmark 35 priority 265
echo "delete drop 28 to 30"
ip rule del blackhole fwmark 36 priority 266


echo "add 30 to 28"
ip rule add fwmark 35 table port14Filters priority 265
echo "add 28 to 30"
ip rule add fwmark 36 table port12Filters priority 266
