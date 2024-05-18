
'''
	from ..utilities.map.etch import etch_map
	etch_map ({
		"path": "",
		"bracket": {}
	})
'''

import json
def etch_map (packet):
	path = packet ["path"]
	bracket = packet ["bracket"]

	with open (path, "w") as FP:
		json.dump (bracket, FP, indent = 4)
		
	return 