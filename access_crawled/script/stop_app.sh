#!/bin/sh


kill -9 -$(ps x -o '%r %a' | grep 'python ../application.py' | grep -v 'grep' | head -1 | awk '{ print $1 }')


# vim:noet:ts=4:sw=4
