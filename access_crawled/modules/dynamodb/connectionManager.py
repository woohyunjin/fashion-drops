# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

from setupDynamoDB		  import getDynamoDBConnection
from boto.dynamodb2.table   import Table
from uuid				   import uuid4

class ConnectionManager:
	def __init__(self, mode=None, config=None, endpoint=None, port=None, use_instance_metadata=False, scheme=None):
		self.db = None
		self.productTable = None
		self.mallTable = None
		
		if mode == "local":
			if config is not None:
				raise Exception('Cannot specify config when in local mode')
			if endpoint is None:
				endpoint = 'localhost'
			if port is None:
				port = 8000
			self.db = getDynamoDBConnection(endpoint=endpoint, port=port, local=True)
		elif mode == "service":
			self.db = getDynamoDBConnection(config=config, endpoint=endpoint, use_instance_metadata=use_instance_metadata)
		else:
			raise Exception("Invalid arguments, please refer to usage.");
		
		if scheme:
			self.schemeLoader = scheme
			self.setupTable(scheme)

	def setupTable(self, schemeLoader):
		cur_table = ''
		tables = {}

		for (name, model) in schemeLoader.models.iteritems():
			cur_table = model.table

			try:
				tables[cur_table] = Table(cur_table, connection=self.db)
				print >> sys.stderr, 'Table %s exist - load table from dynamoDB' % cur_table
			except Exception, e:
				print >> sys.stderr, "%s Table doesn't exist." % cur_table

		self.mallTable = tables['Mall']
		self.productTable = tables['Product']

	def getProductTable(self):
		if self.productTable == None:
			self.setupTable()
		return self.productTable
	
	def getMallTable(self):
		if self.mallTable == None:
			self.setupTable()
		return self.mallTable

# vim: ts=4 sw=4 smarttab smartindent noexpandtab
