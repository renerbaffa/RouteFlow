#!/bin/bash

	user=`whoami`

	if [ "$whoami" == root]
	then
		wget http://packages.couchbase.com/releases/2.0.1/couchbase-server-enterprise_x86_2.0.1.deb
		dpkg -i http://packages.couchbase.com/releases/2.0.1/couchbase-server-enterprise_x86_2.0.1.deb
	else
		echo "You must be a root user."
	fi

exit 0
