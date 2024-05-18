

'''
	from ..utilities.map.etch import scan_map
	scan_map ({
		"path": "",
		"bracket": {}
	})
'''

import json
def scan_map (packet):
	path = packet ["path"]
	bracket = packet ["bracket"]

	with open (path, "w") as FP:
		json.dump (bracket, FP, indent = 4)
		
	return 