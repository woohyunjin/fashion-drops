# -*- coding: utf-8 -*-
import os

SERVICE_NAME = 'accessfdrops'
API_VERSION = 1
API_PATH = '/{0}/api/v{1}'.format(SERVICE_NAME, API_VERSION)

#TWILIO
TWILIO_ACCOUNT_SID = 'AC0999cf52f6ddb975b353d5233b7a1990'
TWILIO_AUTH_TOKEN = '8be6de7aa401de0063ff050587a0d17c'
TWILIO_NUMBER = '+14154844412'

#PARSE
PARSE_APP_ID = 'eJluVDM97PGhOikgvtdj4qPlaieXJS8IU8rfQS7j'
PARSE_REST_API_KEY = 'sV3oiqe7cSwKquY59eP1gFMRJk7HWdG4IZJc65U6'
PARSE_HEADER = {'X-Parse-Application-Id': PARSE_APP_ID,
				'X-Parse-REST-API-Key': PARSE_REST_API_KEY,
				'Content-Type': 'application/json'}

FAKE_USERS = {'fdrops': 'ab3e7c47aac515a5502005e2ffe55ace233f9f90'}			# SHA1 encrypted

#MYSQL
HDB_CONFIG = {
	'user': 'irteam',
	'password': 'hive@2',
	'host': 'localhost',
	'database': 'hivedb',
	'raise_on_warnings': True,
}

# TODO : absoulute path -> relative path
BRIDGE_TOPDIR=os.environ.get('BRIDGE_TOPDIR', '/home1/irteam/Bridge-backend')
JOBCTG_FILE = "{0}/resource/category.txt".format(BRIDGE_TOPDIR)

DEFAULT_PHOTO_EXTENSION = '.png'


# vim:noet:ts=4:sw=4
