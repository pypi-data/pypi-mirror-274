

'''
	from ventures.plays_venture.is_on import venture_is_on
	venture_is_on ({
		"venture": {},
		"ventures_map_bracket": {}
	})
'''

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
from ventures.utilities.ventures.find_venture import find_venture
#
#++++

def venture_is_on (packet):
	name = packet ["name"]
	ventures = packet ["ventures"]
	venture_map_details = packet ["venture_map_details"]
	
	kind = venture_map_details ["kind"]
	
	if (kind == "process_identity"):
		process_identity = venture_map_details ["process_identity"]
		status = check_is_on (process_identity)
		return {
			"process_identity": process_identity,
			"status": status
		}
		
	if (kind == "task"):	
		venture = find_venture (ventures, name)
		status = venture ["is on"] ()			
		return {
			"status": status
		}	

	raise Exception (f"Kind '{ kind }' was not found.")