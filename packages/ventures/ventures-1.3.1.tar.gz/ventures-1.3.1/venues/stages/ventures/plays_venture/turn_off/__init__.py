
'''
	turn_off_venture ({
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
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map	
from ventures.utilities.ventures.find_venture import find_venture
from ventures.utilities.process.check_is_on import check_is_on
#
#
import rich
#
#
import json
import signal
import os
import time
#
#++++

def turn_off_venture (packet):
	venture = packet ["venture"]
	ventures_map_bracket = packet ["ventures_map_bracket"]

	kind = venture ["kind"]
	name = venture ["name"]
	
	print ("venture:", venture)
	
	rich.print_json (data = {
		"play": "turn off",
		"venture": venture,
		"ventures_map_bracket": ventures_map_bracket,
		"name": name
	})

	venture = ventures_map_bracket [name]

	if (kind == "process_identity"):
		if (venture ["process_identity"] != ""):
			process_identity = venture ["process_identity"]
		
			rich.print_json (data = {
				"play": "turn off",
				"process_identity": check_is_on (process_identity)
			})
				
			if (check_is_on (process_identity) != "off"):
				os.kill (process_identity, signal.SIGTERM)
				ventures_map_bracket [ name ] ["process_identity"] = ""
				
				#to_delete.append (name)
				loop = 0
				while True:
					status = check_is_on (process_identity)	
					rich.print_json (data = {
						"play": "turn off",
						"status check cycle": {
							"name": name,
							"status": status
						}
					})
					
					if (status == "off"):
						break;
					
					time.sleep (1)

					loop += 1
					if (loop == 10):
						raise Exception (
							f"After { loop } loops, { name } did not turn off."
						)
				
		
	if (kind == "task"):
		if (venture ["is on"] () != "off"):			
			venture ["turn off"] ()
			
			loop = 0
			while True:
				status = venture ["is on"] ()		

				rich.print_json (data = {
					"venture status check loop": {
						"when": "after turn off was sent",
						"loop": loop,
						"name": venture ["name"],
						"status": status
					}
				})
				
				if (status == "off"):
					break;
				
				time.sleep (1)

				loop += 1
				if (loop == 10):
					raise Exception (
						f"After { loop } loops, { name } did not turn off."
						
					)