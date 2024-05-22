











'''
	from vaccines.mixes.ventures_map.hike_passive import hike_passive
	hike_passive ({
		"script": [
		
		]
	})
'''

'''
	https://stackoverflow.com/a/13593257
'''

#++++
#
from ventures.utilities.hike_passive_p_expect import hike_passive_p_expect
from ventures.utilities.hike_passive_p_expect_2.implicit import process_on_implicit
#
#
import rich
#
#
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit
#
#++++

#
#	tethered
#
def explicit (script):
	the_process = subprocess.Popen (script)
	atexit.register (lambda: the_process.terminate ())
	time.sleep (5)
	
	return the_process
	
#
#	floating,
#	untethered
#
def implicit (script):
	the_process = subprocess.Popen (
		script
	)
	return the_process

def hike_passive (packet):
	script = packet ["script"]

	detached_process = 0x00000008

	the_process = subprocess.Popen (
		script,
		#start_new_session = True
		
		#
		#	https://stackoverflow.com/a/13593257
		#		Windows
		#
		# creationflags = detached_process,
		
		#
		#	https://stackoverflow.com/a/34459371
		#
		#
		close_fds = True
	)
	'''
	the_process = hike_passive_p_expect ({
		"script": script,
		
		"records_path": ""
	})
	
	quest = process_on_implicit (
		'python3 server.py',
		
		CWD = None,
		env = {}
	)
	quest ["process"].terminate ()	
	'''
	
	print ("the_process:", the_process)
	
	return {
		"process_identity": the_process.pid
	}
