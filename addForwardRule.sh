#!/bin/bash

sudo /sbin/iptables -t nat -I PREROUTING -p tcp -d $1 --dport $2 -j DNAT --to-destination $3:80
