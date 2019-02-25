#!/bin/bash

# NFS share comber - checks to see if NFS shares are mountable

# File containing shares should be in the format of 1.1.1.1:/share
# Spool Metasploit NFS mount scanner - scanner/nfs/nfsmount
# Format spool with "grep [+] <SPOOLFILE> | cut -d'-' -f2 | sed 's/NFS Export:/:/g' | sed 's/ //g' | cut -d'[' -f1 > nfs_shares.txt"
# ./nfscomb.sh nfs_shares.txt mnt/

if [ $# -ne 2 ]
then
	echo "Usage: $0 <shares.txt> <mount point>"
	exit 1
else

output="mountable.txt"

touch $output

for share in $(cat $1); do
	echo "Checking share "$share"..."
	for ver in $(seq 2 4); do
		timeout 8s mount -t nfs -onolock,ro,vers=$ver $share $2 2>/dev/null
		if [ $(mount | grep $share | wc -l) -eq 1 ]
		then
			echo -e "\e[32m$share can be mounted using NFS version $ver\e[0m"
			echo "$share - NFS Version: $ver"  >> $output
			umount $2
			sleep 6  # Recommended not to set below 6
			break
		else
			echo -e "\e[31m$share is not mountable using NFS version $ver\e[0m"
		fi
	done
done
fi
