#!/bin/sh +x

mkdir -p ../log

export PYTHONPATH=${PYTHONPATH}:../modules

nohup ~/bin/python ../application.py --mode service --serverPort 5000 --port 8000 \
		  --config ../config --scheme ../modules/models/model.scheme \
	 > ../log/$(date +%y%m%d).log 2>&1 &
	
# vim:noet:ts=4:sw=4
