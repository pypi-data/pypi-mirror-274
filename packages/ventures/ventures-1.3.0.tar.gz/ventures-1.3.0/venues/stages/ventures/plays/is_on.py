
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
	for adventure in ventures_map_bracket:
		adventure_details = ventures_map_bracket [ adventure ]
		kind = adventure_details ["kind"]
		#print (ventures)
		
		if (kind == "process_identity"):
			process_identity = adventure_details ["process_identity"]
			status = check_is_on (process_identity)
			
			statuses [ adventure ] = {
				"process_identity": process_identity,
				"status": status
			}
			
			continue;
			
		if (kind == "task"):	
			venture = find_venture (ventures, adventure)
			status = venture ["is on"] ()
				
			statuses [ adventure ] = {
				"status": status
			}	
				
			continue;
			
		raise Exception (f'Kind "{ kind }" not found.')
				
	rich.print_json (data = {
		"statuses": statuses
	})

	return;	

