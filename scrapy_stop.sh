#!/bin/sh
if [ $# -ne 0 ]; then
	printf "Usage: `basename $0`\n"
	echo $#
	exit 1
fi

function check_fail(){
	if [ $? -ne 0 ]; then
		exit $?
	fi
}

SCRAPY_PATH=`which scrapy`

for pid in $(ps ax | grep ${SCRAPY_PATH} | grep -v grep | awk '{print $1}'); do
	#echo ${pid}
	kill -9 ${pid}
done

echo "SCRAPY STOPPED!" 
# vim:noet:ts=4:sw=4
