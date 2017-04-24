#!/bin/bash
#$1: vmName
#$2: username
#$3: hostIP
sudo virsh migrate --live --persistent $1 qemu+ssh://$2@$3/system
sudo virsh start $1
