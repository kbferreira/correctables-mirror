#!/bin/bash

inject_dir="/sys/kernel/debug/apei/einj"    # root of error inject ...

if [ -d "${inject_dir}" ]
then
	echo 0x12345000 > /sys/kernel/debug/apei/einj/param1 # Set memory address for injection
	echo $((-1 << 12)) > /sys/kernel/debug/apei/einj/param2 # Mask 0xfffffffffffff000 - 
								# anywhere in this page
	echo 0x8 > /sys/kernel/debug/apei/einj/error_type	# Choose correctable memory error
	echo 1 > /sys/kernel/debug/apei/einj/error_inject	# Inject now
else
	echo "APEI Error Injection support not loaded"
fi
