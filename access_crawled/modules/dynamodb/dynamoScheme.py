#!/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging

import traceback

from collections import *
from boto.dynamodb2 import types as schema_types

class dynamoSchemeLoader:
	def __init__(self, fpScheme):
		mdict = {}
		curdata = []

		for line in fpScheme:
			line = line.strip()
			if line.startswith('#'):
				continue
			if not line:
				continue

			if line.startswith('[') and line.endswith(']'):
				if curdata:
					model = self.__parse_data(curdata)
					if model:
						mdict[model.table] = model

			curdata.append(line)

		if curdata:
			model = self.__parse_data(curdata)
			if model:
				mdict[model.table] = model

		self.models = mdict
	
	@staticmethod
	def __parse_data(lines):
		table = ''
		hashKey = ''
		rangeKey = ''
		gIndexes = []
		lIndexes = []
		attributes = []
		keyAttrs = []

		for line in lines:
			# TABLE NAME
			if line.startswith('[') and line.endswith(']'):
				table = line[1:-1]

			# HASH/RANGE KEY PAIR
			elif line.startswith('KEY:'):
				line = line[len('KEY:'):].strip()

				ts = line.split(' ')
				if len(ts) == 1:
					hashKey = ts[0]
					attributes.append(ts[0])
					keyAttrs = [ts[0]]
				else:
					(hashKey, rangeKey) = (ts[0], ts[1])
					attributes.append(ts[0])
					attributes.append(ts[1])
					keyAttrs = [ts[0], ts[1]]

			# GLOBAL INDEX	
			elif line.startswith('GLOBAL:'):
				line = line[len('GLOBAL:'):].strip()

				ts = line.split(' ')
				if len(ts) == 1:
					attributes.append(ts[0])
					
					idxmodel = dynamoGlobalIndex(hashkey=ts[0],
										attributes=list(keyAttrs))
					gIndexes.append(idxmodel)
				elif len(ts) > 1:
					attributes.append(ts[0], ts[1])

					idxmodel = dynamoGlobalIndex(hashkey=ts[0],
										rangekey=ts[1],
										attributes=list(keyAttrs))
					gIndexes.append(idxmodel)
	
			# LOCAL INDEX
			elif line.startswith('LOCAL:'):
				line = line[len('LOCAL:'):].strip()

				ts = line.split(' ')
				if len(ts) > 0:
					attributes.append(lkey)

					idxmodel = dynamoLocalIndex(rangekey=ts[0],
										attributes=list(keyAttrs))
					lIndexes.append(idxmodel)

			# ATTRIBUTES
			elif ':' not in line:
				line = line.strip()

				attr = ''
				ts = line.split(' ')
				if len(ts) == 1:
					attr = ts[0]

				if attr:
					attributes.append(attr)

			# INVALID LINES
			else:
				continue

		# Check if model is valid or not
		if not table or not hashKey:
			return None

		attributes = list(set(attributes))

		return dynamoModel(table=table, 
					hashKey=hashKey,
					rangeKey=rangeKey,
					globalIndexes=gIndexes,
					localIndexes=lIndexes,
					attributes=attributes
					)

class dynamoGlobalIndex:
	def __init__(self, hashkey='', rangekey='', attributes=[]):
		self.name = 'global_' + hashkey
		if rangekey:
			self.name = self.name + '_' + rangekey
		
		self.hashKey = dynamoField(hashkey)
		self.rangeKey = dynamoField(rangekey)
		self.attributes = [dynamoField(attr) for attr in attributes]

class dynamoLocalIndex:
	def __init__(self, rangekey='', attributes=[]):
		self.name = 'local_' + rangekey
		
		self.rangeKey = dynamoField(rangeKey)
		self.attributes = [dynamoField(attr) for attr in attributes]

class dynamoModel:
	def __init__(self, table='', hashKey='', rangeKey='', globalIndexes=[], localIndexes=[], attributes=[]):
		self.table = table
		self.hashKey = dynamoField(hashKey)
		self.rangeKey = dynamoField(rangeKey)
		self.globalIndexes = globalIndexes
		self.localIndexes = localIndexes
		self.attributes = [dynamoField(attr) for attr in attributes]

		self.indexMap = {}
		for gidx in globalIndexes:
			self.indexMap[gidx.hashKey] = gidx
		for lgdx in localIndexes:
			self.indexMap[lidx.hashKey] = lidx

class dynamoField:
	def __init__(self, name=''):
		ts = name.split(':')
		
		if len(ts) == 1:
			self.name = ts[0]
			self.__set_ftype('STRING')
		elif len(ts) > 1:
			self.name = ts[0]
			self.__set_ftype(ts[1])
		else:
			(self.name, self.ftype) = ('', None)

	def __set_ftype(self, typename):
		if not typename:
			typename = 'STRING'
		typename = typename.upper()
		
		try:
			exec 'self.ftype = schema_types.{0}'.format(typename)
		except:
			self.ftype = schema_types.STRING

# vim: ts=4 sw=4 smarttab smartindent noexpandtab
