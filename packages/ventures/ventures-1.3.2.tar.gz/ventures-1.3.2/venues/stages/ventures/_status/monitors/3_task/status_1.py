


'''
	_status/monitors/3_task/status_1.py
'''

from ventures import ventures_map

import requests

import os
import pathlib
from os.path import dirname, join, normpath
import sys
import time

from sanique.adventure import sanique_adventure
sanique_adventure ()

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
			sanique_adventure ()
		]
	})
	
	ventures ["turn on"] ()
	
	#time.sleep (10)

	response = requests.get ("http://0.0.0.0:10000")
	assert (response.status_code == 404)
	
	
	ventures ["turn off"] ()
	
	#time.sleep (10)
	
checks = {
	'check 1': check_1
}