#!/bin/bash

	user=`whoami`

	if [ "$user" == "root" ]
	then
		wget -O /etc/apt/sources.list.d/couchbase.list http://packages.couchbase.com/ubuntu/couchbase-ubuntu1204.list
		wget -O- http://packages.couchbase.com/ubuntu/couchbase.key | apt-key add -
		apt-get update
		apt-get install libcouchbase2 libcouchbase-dev python-pip python-dev
		pip install couchbase
	else
		echo "You must be a root user."
	fi

exit 0
