


'''
	from ..utilities.map.scan import scan_map
	the_map_path = scan_map ({
		"path": ""
	})
'''

import json
def scan_map (packet):
	path = packet ["path"]

	with open (path, "r") as FP:
		the_map_path = json.load (FP)
		
	return the_map_path