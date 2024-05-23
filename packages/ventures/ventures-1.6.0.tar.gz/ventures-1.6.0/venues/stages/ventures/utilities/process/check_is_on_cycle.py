

'''
	from .check_is_on_cycle import check_is_on_cycle
	check_is_on_cycle ({
		"process_identity": "123",
		"wait_for": "on"
	})
'''

import time
from ventures.utilities.check_is_on import check_is_on

def check_is_on_cycle (packet):
	process_identity = packet ["process_identity"]
	wait_for = packet ["wait_for"]

	loop = 0
	while True:
		the_status = check_is_on (process_identity)
		if (the_status == wait_for):
			break;
		
		time.sleep (1)

		loop += 1
		if (loop == 10):
			raise Exception (
				f"An anomaly occurred: { name } is { the_status } instead of { wait_for }"
			)