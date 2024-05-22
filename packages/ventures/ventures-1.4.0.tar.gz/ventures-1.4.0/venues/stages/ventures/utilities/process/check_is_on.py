
'''
	from ventures.utilities.pocess.check_is_on import check_is_on
	status = check_is_on (pid)
'''

import psutil

def is_process_defunct(pid):
	try:
		process = psutil.Process(pid)
		return process.status() == psutil.STATUS_ZOMBIE
	except psutil.NoSuchProcess:
		return False

def check_is_on (pid):
	try:
		if (pid == ""):
			return "off"
	
		pid = int (pid)
		
		#print ("checking on pid:", pid)
		
		is_defunct = is_process_defunct (pid)
		if (is_defunct == True):
			return "off"
		
		exists = psutil.pid_exists (pid)
		if (exists == True):
			return "on"
		
		return "off"

	except Exception as E:
		print ("process status exception :", E)
		
	return "unknown";
