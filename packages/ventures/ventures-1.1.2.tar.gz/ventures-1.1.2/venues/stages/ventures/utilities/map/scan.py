


'''
	from ..utilities.map.scan import scan_map
	the_map = scan_map ({
		"path": ""
	})
'''

import json
def scan_map (packet):
	path = packet ["path"]

	with open (path, "r") as FP:
		the_map = json.load (FP)
		
	return the_map