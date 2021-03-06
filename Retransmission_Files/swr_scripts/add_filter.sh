
wuIf=$(netstat -ie | grep -B1 "192.168.28.2" | head -n1 | awk '{print $1}')
uiucIf=$(netstat -ie | grep -B1 "192.168.30.2" | head -n1 | awk '{print $1}')

iptables -t mangle -I PREROUTING -d 192.168.28.0/24 -s 192.168.30.0/24 -j MARK --set-mark 60
iptables -t filter -A FORWARD -d 192.168.28.0/24 -s 192.168.30.0/24 -j MARK --set-mark 60
tc filter add dev $wuIf parent 13:0 protocol ip prio 2 handle 60 fw flowid 13:57
ip rule add fwmark 60 table port12Filters priority 300


iptables -t mangle -I PREROUTING -d 192.168.30.0/24 -s 192.168.28.0/24 -j MARK --set-mark 61
iptables -t filter -A FORWARD -d 192.168.30.0/24 -s 192.168.28.0/24 -j MARK --set-mark 61
tc filter add dev $uiucIf parent 15:0 protocol ip prio 2 handle 61 fw flowid 15:56
ip rule add fwmark 61 table port14Filters priority 301
