

from ..utilities.hike_passive import hike_passive
from ..utilities.map.etch import etch_map
	

'''
	{
		"name": "adventure_1",
		"turn on": {
			"adventure": "python3 -m http.server 8080",
			"kind": "process_identity"
		}
	}
'''
def turn_on (packet):
	print ("packet:", packet)
	ventures = packet ["ventures"]
	the_map = packet ["map"]

	ventures_map_bracket = {}
	for adventure in ventures:
		adventure_script = adventure ["turn on"] ["adventure"]
		kind = adventure ["turn on"] ["kind"]
		name = adventure ["name"]
	
		process = hike_passive ({
			"script": adventure_script
		})
		
		if (kind == "process_identity"):
			ventures_map_bracket [ name ] = {
				"kind": kind,
				"process_identity": process ["process_identity"]
			}
		
		else:
			ventures_map_bracket [ name ] = {
				"kind": kind
			}

	
	etch_map ({
		"path": the_map,
		"bracket": ventures_map_bracket
	})
	
	return ventures_map_bracket