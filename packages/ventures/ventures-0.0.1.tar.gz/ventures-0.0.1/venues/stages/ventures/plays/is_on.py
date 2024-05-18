

'''
	# Replace 'your_pid_here' with the actual PID you want to check
	pid_to_check = your_pid_here
	status = check_process_status (pid_to_check)
	print ("Process status:", status)
'''
import psutil
import time
import json


from ventures.utilities.process.check_is_on import check_is_on

	
def is_on (packet):
	the_map = packet ["the_map"]
	
	with open (the_map, 'r') as FP:
		bracket = json.load (FP)
	
	#print ("bracket:", bracket)
	
	print ()
	print ("status:")
	
	for adventure in bracket:
		adventure_details = bracket [ adventure ]
		
		process_identity = adventure_details ["process_identity"]
		status = check_is_on (process_identity)
		print (f'    [{ status }] :: "{ adventure }" { process_identity }"')
		
	print ()

	return;	

