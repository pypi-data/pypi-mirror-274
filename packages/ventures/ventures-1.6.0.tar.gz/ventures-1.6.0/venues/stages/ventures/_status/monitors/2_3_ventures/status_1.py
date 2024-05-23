
'''
	_status/monitors/status_1.py
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
				"name": "adventure_1",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"9080"
					],
					"Popen": {},
				}
			},
			{
				"name": "adventure_2",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"9081"
					],
					"Popen": {},
					
				}
			},
			{
				"name": "adventure_3",
				"kind": "process_identity",
				"turn on": {
					"adventure": [ 
						"python3",
						"-m",
						"http.server",
						"9082"
					],
					"Popen": {}
				}
			}
		]
	})
	
	ventures ["turn on"] ()
	
	time.sleep (1)

	response = requests.get("http://0.0.0.0:9080")
	assert (response.status_code == 200)

	response = requests.get("http://0.0.0.0:9081")
	assert (response.status_code == 200)
	
	response = requests.get("http://0.0.0.0:9082")
	assert (response.status_code == 200)

	ventures ["turn off"] ()
	
	
checks = {
	'check 1': check_1
}