


'''
	_status/monitors/5_refresh_1/status_1.py
'''

from ventures import ventures_map

import requests

import os
import pathlib
from os.path import dirname, join, normpath
import sys
import time

def ensure_cannot_connect (address):
	connection_exception = "no"
	try:
		response = requests.get (address)
	except requests.exceptions.ConnectionError:
		connection_exception = "yes"
		
	assert (connection_exception == "yes")

def check_1 ():
	this_folder = pathlib.Path (__file__).parent.resolve ()
	the_map_path = str (
		normpath (join (
			this_folder, 
			"ventures_map.JSON"
		))
	)
	
	print ("the_map_path:", the_map_path)
	
	ventures = ventures_map ({
		"map": the_map_path,
		"ventures": [
			{
				"name": "quest_1",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"15000"
					],
					"Popen": {},
				}
			},
			{
				"name": "quest_2",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"15001"
					],
					"Popen": {},
				}
			},
		]
	})
	
	ventures ["turn on"] ()
	time.sleep (1)
	assert (requests.get ("http://0.0.0.0:15000").status_code == 200)
	assert (requests.get ("http://0.0.0.0:15001").status_code == 200)
	
	#
	#
	#
	#
	ventures ["turn off"] ({ "name": "quest_1" })
	ensure_cannot_connect ("http://0.0.0.0:15000")
	assert (requests.get ("http://0.0.0.0:15001").status_code == 200)

	
	ventures ["turn off"] ()
	ensure_cannot_connect ("http://0.0.0.0:15000")
	ensure_cannot_connect ("http://0.0.0.0:15001")

	ventures ["turn on"] ({ "name": "quest_2" })
	time.sleep (1)
	ensure_cannot_connect ("http://0.0.0.0:15000")
	assert (requests.get ("http://0.0.0.0:15001").status_code == 200)

	ventures ["turn off"] ()
	ensure_cannot_connect ("http://0.0.0.0:15000")
	ensure_cannot_connect ("http://0.0.0.0:15001")

checks = {
	'check 1': check_1
}