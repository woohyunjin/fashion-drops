import sys

from boto.exception         import JSONResponseError
from boto.dynamodb2.fields  import KeysOnlyIndex
from boto.dynamodb2.fields  import GlobalAllIndex, GlobalKeysOnlyIndex
from boto.dynamodb2.fields  import HashKey
from boto.dynamodb2.fields  import RangeKey
from boto.dynamodb2.layer1  import DynamoDBConnection
from boto.dynamodb2.table   import Table
from boto.dynamodb2.types	import *

from dynamoScheme			import dynamoSchemeLoader 

import urllib2, json

def getDynamoDBConnection(config=None, endpoint=None, port=None, local=False, use_instance_metadata=False):
    if local:
        db = DynamoDBConnection(
            host=endpoint,
            port=port,
            aws_secret_access_key='poukm1mqgzmxVorKJ3uDi6V5SxoagTjrEugF03ai', 
            aws_access_key_id='AKIAINGMFG3VFUJFXF4A',   
            is_secure=False)
    else:
        params = {
            'is_secure': True
            }

        # Read from config file, if provided
        if config is not None:
            if config.has_option('dynamodb', 'region'):
                params['region'] = config.get('dynamodb', 'region')
            if config.has_option('dynamodb', 'endpoint'):
                params['host'] = config.get('dynamodb', 'endpoint')

            if config.has_option('dynamodb', 'aws_access_key_id'):
                params['aws_access_key_id'] = config.get('dynamodb', 'aws_access_key_id')
                params['aws_secret_access_key'] = config.get('dynamodb', 'aws_secret_access_key')

        # Use the endpoint specified on the command-line to trump the config file
        if endpoint is not None:
            params['host'] = endpoint
            if 'region' in params:
                del params['region']

        # Only auto-detect the DynamoDB endpoint if the endpoint was not specified through other config
        if 'host' not in params and use_instance_metadata:
            response = urllib2.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read()
            doc = json.loads(response);
            params['host'] = 'dynamodb.%s.amazonaws.com' % (doc['region'])
            if 'region' in params:
                del params['region']

        db = DynamoDBConnection(**params)
    return db

def setTablesdb(db, schemeLoader):
	cur_table = ''
	tables = {}

	for (name, model) in schemeLoader.models.iteritems():
		cur_table = model.table
		try:
			schema = [HashKey(model.hashKey.name, data_type=model.hashKey.ftype)]
			if model.rangeKey:
				schema.append(RangeKey(model.rangeKey.name, data_type=model.rangeKey.ftype))
		
			gindexes = []
			for gidx in model.globalIndexes:
				parts = [HashKey(gidx.hashKey.name, data_type=gidx.hashKey.ftype)]
				if gidx.rangeKey:
					parts.append(RangeKey(gidx.rangeKey.name, 
										data_type=gidx.rangeKey.ftype))
				gindexes.append(GlobalKeysOnlyIndex(gidx.name, parts=parts,
										throughput={'read': 10, 'write': 10}))

			#TODO : Implement
			for lidx in model.localIndexes:
				pass

			table = Table.create(cur_table, 
								schema=schema,
								throughput={'read': 10, 'write': 10}, 
								global_indexes=gindexes,
								connection=db)

			tables[cur_table] = table
		except JSONResponseError, jre:
			try:
				tables[cur_table] = Table(cur_table, connection=db)
			except Exception, e:
				print >> sys.stderr, "%s Table doesn't exist." % cur_table

	return tables

# vim: ts=4 sw=4 smarttab smartindent noexpandtab
