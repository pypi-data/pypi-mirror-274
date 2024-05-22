
#++++
#
from ventures.utilities.hike_passive import hike_passive
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map	
from ventures.utilities.ventures.find_venture import find_venture
#
from ventures.utilities.process.check_is_on import check_is_on
#
from ventures.plays_venture.turn_on import turn_on_venture

#
#
import rich
#
#
import os
import time
#
#++++

''''
	{
		"name": "adventure_1",
		"turn on": {
			"adventure": "python3 -m http.server 8080",
			"kind": "process_identity",
			"Popen": {
				"CWD": 
			},
		}
	}
	
	{
		"name": "adventure_2",
		"turn on": {
			"adventure": turn_on,
			"kind": "task"
		}
	}
"'''


def turn_on (packet):
	ventures = packet ["ventures"]
	ventures_map_bracket = packet ["ventures_map_bracket"]
	
	for adventure in ventures:
		turn_on_venture ({
			"venture": adventure,
			"ventures_map_bracket": ventures_map_bracket
		})
		
		continue;
	
	return {
		"ventures_map_bracket": ventures_map_bracket
	}
	
