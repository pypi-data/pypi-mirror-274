
'''
	_status/monitors/1_1_venture/status_1.py
'''

from ventures import ventures_map

import requests

import os
import pathlib
from os.path import dirname, join, normpath
import sys
import time

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
				"name": "1_1_venture_python3_http",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"8080"
					],
					"Popen": {},
				}
			},
		]
	})
	
	ventures ["turn on"] ()
	
	#
	#
	#
	#
	
	time.sleep (1)
	response = requests.get ("http://0.0.0.0:8080")
	assert (response.status_code == 200)

	#
	#
	#
	#

	ventures ["turn off"] ()
	
	#
	#
	#
	#
	
	time.sleep (1)
	connection_exception = "no"
	try:
		response = requests.get ("http://0.0.0.0:8080")
	except requests.exceptions.ConnectionError:
		connection_exception = "yes"
		
	assert (connection_exception == "yes")
	
	
	
checks = {
	'check 1': check_1
}