

'''
	turn_off ({
		
	})
'''

import json
import signal
import os

from ..utilities.map.scan import scan_map

def turn_off (packet):
	the_map = packet ["the_map"]
	with open (the_map, 'r') as FP:
		bracket = json.load (FP)

	print ("bracket:", bracket)
	
	for name in bracket:
		adventure = bracket [ name ]
		kind = adventure ["kind"]
		
		print ("kind:", kind)
		
		if (kind == "process_identity"):
			process_identity = adventure ["process_identity"]
			
			os.kill (process_identity, signal.SIGTERM)
			
			