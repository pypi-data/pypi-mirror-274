









'''
	from vaccines.mixes.ventures_map.hike_passive import hike_passive
	hike_passive (
		script = [
		
		]
	)
'''

import rich
	
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit

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

	the_process = subprocess.Popen (
		script
	)
	
	print ("the_process:", the_process)
	
	return {
		"process_identity": the_process.pid
	}
