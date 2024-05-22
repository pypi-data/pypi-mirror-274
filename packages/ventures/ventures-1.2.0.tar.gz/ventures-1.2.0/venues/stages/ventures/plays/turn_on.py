
#++++
#
from ..utilities.hike_passive import hike_passive
from ..utilities.map.etch import etch_map
from ..utilities.map.scan import scan_map	
from ..utilities.ventures.find_venture import find_venture
#
from ventures.utilities.process.check_is_on import check_is_on
#
#
import rich
#
#
import os
import time
#
#++++

'''
	{
		"name": "adventure_1",
		"turn on": {
			"adventure": "python3 -m http.server 8080",
			"kind": "process_identity",
			"Popen": {
				"CWD": 
			},
		}
	}
	
	{
		"name": "adventure_2",
		"turn on": {
			"adventure": turn_on,
			"kind": "task"
		}
	}
'''


def turn_on (packet):
	ventures = packet ["ventures"]
	the_map_path = packet ["map"]
	
	

	ventures_map_bracket = {}
	if os.path.exists (the_map_path):
		ventures_map_bracket = scan_map ({
			"path": the_map_path
		})

	for adventure in ventures:
		adventure_script = adventure ["turn on"] ["adventure"]
		kind = adventure ["kind"]
		name = adventure ["name"]
		
		
		#
		#	check if is already on	
		#
		#
		if (name in ventures_map_bracket):
			if (kind == "process_identity"):
				if (ventures_map_bracket [ name ] ["process_identity"] != ""):
					status = check_is_on (ventures_map_bracket [ name ] ["process_identity"])
					if (status == "on"):
						#print (f'"{ name }" is already on')
						continue;
			
			if (kind == "task"):
				venture = find_venture (ventures, name)
				status = venture ["is on"] ()
				if (status == "on"):
					continue;

		
		
		if (kind == "process_identity"):
			print ("adventure:", adventure)
		
			Popen_keys = {}
			if ("turn on" in adventure):
				if ("Popen" in adventure ["turn on"]):
					if (type (adventure ["turn on"] ["Popen"]) == dict):
						Popen_keys = adventure ["turn on"] ["Popen"]
		
			process = hike_passive ({
				"script": adventure_script,
				"Popen": Popen_keys
			})
			
			loop = 0
			while True:
				status = check_is_on (process ["process_identity"])	
				rich.print_json (data = {
					"venture status check loop": {
						"when": "after turn on was sent",
						"loop": loop,
						"name": name,
						"status": status
					}
				})
				
				if (status == "on"):
					break;
				
				time.sleep (1)

				loop += 1
				if (loop == 10):
					raise Exception (
						f"After { loop } loops, { name } did not turn on."
					)
		
			ventures_map_bracket [ name ] = {
				"kind": kind,
				"process_identity": process ["process_identity"]
			}
		
			continue;
			
		if (kind == "task"):
			adventure_script ()
			
			loop = 0
			while True:
				status = adventure ["is on"] ()		
				rich.print_json (data = {
					"venture status check loop": {
						"when": "after turn on was sent",
						"loop": loop,
						"name": name,
						"status": status
					}
				})
				
				if (status == "on"):
					break;
				
				time.sleep (1)

				loop += 1
				if (loop == 10):
					raise Exception (
						f"After { loop } loops, { name } did not turn on."
					)
			
			ventures_map_bracket [ name ] = {
				"kind": kind
			}
			
		
		else:
			raise Exception (f'Kind "{ kind } was not found.')

	
	etch_map ({
		"path": the_map_path,
		"bracket": ventures_map_bracket
	})
	
	return ventures_map_bracket