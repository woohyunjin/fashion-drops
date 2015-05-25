#!flask/bin/python
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
import sys; sys.path.append('./modules')

from dynamodb.connectionManager	 import ConnectionManager
from dynamodb.dbController		  import DBController
from dynamodb.dynamoScheme		  import dynamoSchemeLoader
from uuid						   import uuid4
from flask						  import Flask, render_template, request, session, flash, redirect, jsonify, json
from ConfigParser				   import ConfigParser
import os, time, argparse


from constant import *

application = Flask(__name__)
application.debug = True
application.secret_key = str(uuid4())
		
"""
   Configure the application according to the command line args and config files
"""

cm = None

parser = argparse.ArgumentParser(description='Access crawled data', prog='application.py')
parser.add_argument('--config', help='Path to the config file containing application settings. Cannot be used if the CONFIG_FILE environment variable is set instead')
parser.add_argument('--mode', help='Whether to connect to a DynamoDB service endpoint, or to connect to DynamoDB Local. In local mode, no other configuration ' \
					'is required. In service mode, AWS credentials and endpoint information must be provided either on the command-line or through the config file.',
					choices=['local', 'service'], default='service')
parser.add_argument('--endpoint', help='An endpoint to connect to (the host name - without the http/https and without the port). ' \
					'When using DynamoDB Local, defaults to localhost. If the USE_EC2_INSTANCE_METADATA environment variable is set, reads the instance ' \
					'region using the EC2 instance metadata service, and contacts DynamoDB in that region.')
parser.add_argument('--scheme', help='DynamoDB table scheme description file')
parser.add_argument('--port', help='The port of DynamoDB Local endpoint to connect to.  Defaults to 8000', type=int)
parser.add_argument('--serverPort', help='The port for this Flask web server to listen on.  Defaults to 5000 or whatever is in the config file. If the SERVER_PORT ' \
					'environment variable is set, uses that instead.', type=int)
args = parser.parse_args()

configFile = args.config
config = None
if 'CONFIG_FILE' in os.environ:
	if configFile is not None:
		raise Exception('Cannot specify --config when setting the CONFIG_FILE environment variable')
	configFile = os.environ['CONFIG_FILE']
if configFile is not None:
	config = ConfigParser()
	config.read(configFile)

# Read environment variable for whether to read config from EC2 instance metadata
use_instance_metadata = ""
if 'USE_EC2_INSTANCE_METADATA' in os.environ:
	use_instance_metadata = os.environ['USE_EC2_INSTANCE_METADATA']

schemeLoader = dynamoSchemeLoader(open(args.scheme))

cm = ConnectionManager(mode=args.mode, config=config, endpoint=args.endpoint, port=args.port, use_instance_metadata=use_instance_metadata, scheme=schemeLoader)
controller = DBController(cm, scheme=schemeLoader)

serverPort = args.serverPort
if config is not None:
	if config.has_option('flask', 'secret_key'):
		application.secret_key = config.get('flask', 'secret_key')
	if serverPort is None:
		if config.has_option('flask', 'serverPort'):
			serverPort = config.get('flask', 'serverPort')

# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
	serverPort = int(os.environ['SERVER_PORT'])

if serverPort is None:
	serverPort = 5000



"""
   Scheme setting/management
"""
@application.route(API_PATH, methods=['GET'])
def show_doc():
	return render_template('api_doc_v{0}.html'.format(API_VERSION))





"""
   Scheme setting/management
"""
@application.route('{0}/health'.format(API_PATH), methods=['GET'])
def check_health():
	return jsonify({'status': 'healthy', })

@application.route('{0}/drop'.format(API_PATH), methods=['GET'])
def resetScheme():
	ret = 'success'
	r = controller.dropTable()
	if r == 'fail':
		ret = 'droptable failed'

	return jsonify({'status': ret, })

@application.route('{0}/create'.format(API_PATH), methods=['GET'])
def setScheme():
	ret = 'success'
	r = controller.createTable()
	if r == 'fail':
		ret = 'createtable failed'
	
	return jsonify({'status': ret, })

"""
   Data check
"""
@application.route('{0}/malls'.format(API_PATH), methods=['GET'])
def get_mall(mall_id):
	argkeys = ['mallName']
	args = {}
	for argkey in argkeys:
		args[argkey] = request.args.get(argkey.lower())
	
	mall = controller.getMall(**args)
	return jsonify({'result' : products})

@application.route('{0}/products'.format(API_PATH), methods=['GET'])
def getProduct():
	argkeys = ['mallName', 'code', 'category', 'limit']
	args = {}
	for argkey in argkeys:
		args[argkey] = request.args.get(argkey.lower())

	products = controller.getProducts(**args)
	
	return jsonify({'result' : products})

"""
   Data insert
"""
@application.route('{0}/products'.format(API_PATH), methods=['POST'])
def insertProduct():
	payload = request.get_json(force=True)

	products = payload['products']
	print >> sys.stderr, products
	try:
		controller.insertProducts(products)
		result = 'success'
	except:
		result = 'fail'
	
	return jsonify({'result' : result})


if __name__ == "__main__":
	if cm:
		application.run(debug = True, port=serverPort, host='0.0.0.0')

# vim: ts=4 sw=4 smarttab smartindent noexpandtab
