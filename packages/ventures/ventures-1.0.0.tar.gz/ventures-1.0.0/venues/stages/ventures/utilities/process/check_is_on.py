
'''
	from ventures.utilities.check_is_on import check_is_on
	status = check_is_on (pid)
'''

import psutil

def check_is_on (pid):
	try:
		if (pid == ""):
			return "off"
	
		pid = int (pid)
	
		exists = psutil.pid_exists (pid)
		if (exists == True):
			return "on"
		
		return "off"

	except Exception as E:
		print ("process status exception :", E)
		
	return "unknown";
