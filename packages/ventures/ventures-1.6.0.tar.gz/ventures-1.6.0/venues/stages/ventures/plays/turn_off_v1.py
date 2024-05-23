

''''
	turn_off ({
		
	})
	
"'''


#++++
#
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map	
from ventures.utilities.ventures.find_venture import find_venture
from ventures.utilities.process.check_is_on import check_is_on
#
from ventures.plays_venture.turn_off import turn_off_venture
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


def turn_off (packet):
	ventures_map_bracket = packet ["ventures_map_bracket"]
	ventures = packet ["ventures"]
	
	to_delete = []
	for name in ventures_map_bracket:
		adventure = ventures_map_bracket [ name ]
		kind = adventure ["kind"]
	
		venture = find_venture (ventures, name)
		
		'''
						"venture": {
				"kind": kind,
				"name": name,
				"turn on": {
					"adventure": adventure
				}
			},
		'''
	
		turn_off_venture ({
			"venture": venture,
			"ventures_map_bracket": ventures_map_bracket
		})
	
		continue;
	
		adventure = ventures_map_bracket [ name ]
		kind = adventure ["kind"]
		
		rich.print_json (data = {
			"play": "turn off",
			"adventure": adventure
		})


		if (kind == "process_identity"):
			if (adventure ["process_identity"] != ""):
				process_identity = adventure ["process_identity"]
			
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
			venture = find_venture (ventures, name)
			
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
				
	#for name in to_delete:
	#	del ventures_map_bracket [ name ]
	
	
	