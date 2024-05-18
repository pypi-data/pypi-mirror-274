

from .utilities.hike_passive import hike_passive


'''
	ventures_map.JSON {
		"adventure_1": {
			"process_identity": ""
		},
		"adventure_2": {
			"process_identity": ""
		}				
	}
'''

'''
	check_is_on ({
		"name": "",
		
		"is_on": 
		"wait_for": 
	})
'''

import rich





	




'''
	ventures_map = scan_map ()
'''

from .plays.turn_on import turn_on
from .plays.turn_off import turn_off
from .plays.is_on import is_on

def ventures_map (packet):
	ventures = packet ["ventures"]
	the_map = packet ["map"]

	def turn_on_move ():
		ventures_map_bracket = turn_on ({
			"ventures": ventures,
			"map": the_map
		})
		
		rich.print_json (data = ventures_map_bracket);
		
		

	def is_on_move ():
		status = is_on ({
			"the_map": the_map
		});
	
		return;
		
	def turn_off_move ():
		turn_off ({
			"the_map": the_map
		});
	
		return;

	return {
		"turn on": turn_on_move,
		"turn off": turn_off_move,
		"is on": is_on_move
	}