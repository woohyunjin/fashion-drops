#!/bin/sh +x

mkdir -p ../log

#PYTHONPATH=../lib/python 
nohup ~/bin/python ../application.py --mode service --serverPort 5000 --port 8000 \
		  --config ../config \
	 > ../log/$(date +%y%m%d).log 2>&1 &
	
# vim:noet:ts=4:sw=4
