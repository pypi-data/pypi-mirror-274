

'''
	turn_on_venture ({
		"venture": {
			"kind": "",
			"name": "",
			"turn on": {
				"adventure": ""
			}
		},
		"ventures_map_bracket": 
	})
'''

#++++
#
from ventures.utilities.map.scan import scan_map
from ventures.utilities.map.etch import etch_map
from ventures.utilities.process.check_is_on import check_is_on
from ventures.utilities.hike_passive import hike_passive
#
from ventures.utilities.ventures.find_venture import find_venture
#
#
import rich
#
#
import os
import time
#
#++++
	
def turn_on_venture (packet):
	venture = packet ["venture"]

	adventure_script = venture ["turn on"] ["adventure"]
	kind = venture ["kind"]
	name = venture ["name"]
	
	ventures_map_bracket = packet ["ventures_map_bracket"]
	
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
					return;
		
		if (kind == "task"):
			#venture = find_venture (ventures, name)
			status = venture ["is on"] ()
			if (status == "on"):
				return;

	
	
	if (kind == "process_identity"):
		print ("venture:", venture)
	
		Popen_keys = {}
		if ("turn on" in venture):
			if ("Popen" in venture ["turn on"]):
				if (type (venture ["turn on"] ["Popen"]) == dict):
					Popen_keys = venture ["turn on"] ["Popen"]
	
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
	
		
		
	elif (kind == "task"):
		adventure_script ()
		
		loop = 0
		while True:
			status = venture ["is on"] ()		
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
		
		
	return 	{
		"ventures_map_bracket": ventures_map_bracket
	}
		
