#!/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging

import traceback

import json

import time
import random

from collections import *

#############
# constants #
#############
SLEEPTIME = 2

SERVERHOST = 'http://54.65.178.128:5000'
SERVERURL = SERVERHOST + '/accessfdrops/api/v1/products'
HEADERS = {
			'user-agent': 'dynamo-insert',
			'Content-Type': 'application/json'
		  }

#################
# main function #
#################
def main(fpin, fpout):
	datalist = []
	datalist2 = []
	datalist.append( 
		{
			'MallName' : 'StyleNanda',
			'Code' : 'xxxTESTxxx56',
			'CategoryMain' : 'HipHop',
		}
	)
	datalist.append( 
		{
			'MallName' : 'StyleNanda',
			'Code' : 'xxxTESTxxx77',
			'CategoryMain' : 'Female',
			'CategoryAll' : ['Female'],
			'ImageUrl' : 'http://naver.com',
			'InsertDateTime' : 1430805875,
			'Name' : 'yyy skirt',
			'Price' : 50000,
			'Url' : 'http://cafe.naver.com'
		}
	)

	res = safe_request(SERVERURL, method='POST', data={'products' : datalist})

	print res

def random_sleep(sleeptime=SLEEPTIME):
	time.sleep(random.randrange(SLEEPTIME,SLEEPTIME + 1))
	return

def safe_request(url, method='GET', data=None):
	import requests
	MAX_ATTEMPT = 1

	req = None
	try_attempt = 0

	while try_attempt < MAX_ATTEMPT:
		try:
			if method == 'GET':
				req = requests.get(url, headers=HEADERS)
			else:
				req = requests.post(url, data=json.dumps(data), headers=HEADERS)
				print >> sys.stderr, req.text
			break
		except Exception as e:
			print >> sys.stderr, 'REQUEST ERROR:%s - waiting for a while' % url
			traceback.print_exc()

			random_sleep(60)
			try_attempt = try_attempt + 1

	random_sleep()

	return req

if __name__ == '__main__': 
	_g_parser = argparse.ArgumentParser(description='echo program like cat')
	_g_parser.add_argument('input', help='input file <default: stdin>',
						nargs='?', type=file, metavar='INPUT FILE', default=sys.stdin)      # positional arguments
	_g_parser.add_argument('--output', help='output file <default: stdout>',
						type=argparse.FileType('w'), metavar='FILE', default=sys.stdout)
	_g_parser.add_argument('--log-level', help='set logging level', metavar='LEVEL')
	_g_parser.add_argument('--log-file', help='set log file <default: stderr>', metavar='FILE')
	_g_args = _g_parser.parse_args()
	_g_log_config = {'format':'[%(asctime)-15s] %(levelname)-8s %(message)s', 'datefmt':'%Y-%m-%d %H:%M:%S'}
	
	if _g_args.log_level:
		_g_log_config['level'] = eval('logging.%s' % _g_args.log_level.upper())
	
	if _g_args.log_file:
		_g_log_config['filemode'] = 'w'     # new empty file
		_g_log_config['filename'] = _g_args.log_file
	logging.basicConfig(**_g_log_config)        # pylint: disable=W0142
	
	main(_g_args.input, _g_args.output)

# column width: 120
# vim: ts=4 sw=4 smarttab smartindent noexpandtab
