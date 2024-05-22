

''''
	turn_off ({
		
	})
	
"'''


#++++
#
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map	
from ventures.utilities.ventures.find_venture import find_venture
from ventures.utilities.process.check_is_on import check_is_on
#
from ventures.plays_venture.turn_off import turn_off_venture
#
#
import rich
#
#
import json
import signal
import os
import time
#
#++++


def turn_off (packet):
	ventures_map_bracket = packet ["ventures_map_bracket"]
	ventures = packet ["ventures"]
	
	for name in ventures_map_bracket:
		turn_off_venture ({
			"venture": find_venture (ventures, name),
			"ventures_map_bracket": ventures_map_bracket
		})
	
	
		
	
	