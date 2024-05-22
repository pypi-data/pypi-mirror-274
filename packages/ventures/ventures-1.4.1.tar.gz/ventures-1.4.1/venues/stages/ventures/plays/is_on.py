
''''
	
"'''

#++++
#
import psutil
import time
import json
#
#
import rich
#
#
from ventures.utilities.process.check_is_on import check_is_on
from ventures.plays_venture.is_on import venture_is_on
#
#++++

def find_venture (ventures, name):
	for venture in ventures:
		if (name == venture ["name"]):
			return venture;
			
	raise Exception (f"Venture with name '{ name }' not found.")
	
	
def is_on (packet):
	ventures_map_bracket = packet ["ventures_map_bracket"]
	ventures = packet ["ventures"]
	
	statuses = {}
	for name in ventures_map_bracket:
		venture_map_details = ventures_map_bracket [ name ]
		
		status = venture_is_on ({
			"name": name,
			"ventures": ventures,
			"venture_map_details": venture_map_details
		})
		
		statuses [ name ] = status;
		
		continue;
		
		kind = venture_map_details ["kind"]
		
		if (kind == "process_identity"):
			process_identity = venture_map_details ["process_identity"]
			status = check_is_on (process_identity)
			statuses [ name ] = {
				"process_identity": process_identity,
				"status": status
			}
			
			continue;
			
		if (kind == "task"):	
			venture = find_venture (ventures, name)
			status = venture ["is on"] ()
			statuses [ name ] = {
				"status": status
			}	
				
			continue;
			
		raise Exception (f'Kind "{ kind }" not found.')
				
	rich.print_json (data = {
		"statuses": statuses
	})

	return;	

