#! /bin/bash

#need to know initial priority and mark
echo "delete 30 to 28"
ip rule del fwmark 60 table port12Filters priority 300
echo "delete 28 to 30"
ip rule del fwmark 61 table port14Filters priority 301


echo "drop 30 to 28"
ip rule add blackhole fwmark 60 priority 300
echo "drop 28 to 30"
ip rule add blackhole fwmark 61 priority 301
