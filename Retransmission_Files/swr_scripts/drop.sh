#! /bin/bash

#need to know initial priority and mark
echo "delete 30 to 28"
ip rule del fwmark 35 table port14Filters priority 265
echo "delete 28 to 30"
ip rule del fwmark 36 table port12Filters priority 266


echo "drop 30 to 28"
ip rule add blackhole fwmark 35 priority 265
echo "drop 28 to 30"
ip rule add blackhole fwmark 36 priority 266
