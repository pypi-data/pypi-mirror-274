









'''
	from ventures.utilities.hike_passive import hike_passive
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
from pydash import merge
#
#
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit
import os
import sys
import subprocess
#
#++++


def hike_passive (packet):
	script = packet ["script"]

	Popen_keys = {}
	if ("Popen" in packet):
		if (type (packet ["Popen"]) == dict):
			Popen_keys = packet ["Popen"]

	def daemonize ():
		# Fork the parent process
		pid = os.fork ()
		if pid > 0:
			# Exit the parent process
			sys.exit (0)

		# Detach from the controlling terminal
		os.setsid ()

		# Fork again to prevent becoming a session leader
		pid = os.fork ()
		if pid > 0:
			# Exit the second parent process
			sys.exit(0)

		# Change the current working directory to root
		os.chdir('/')

		# Set file creation mask
		os.umask (0)

		# Close standard file descriptors
		sys.stdin.close()
		sys.stdout.close()
		sys.stderr.close()

		# Open standard file descriptors to /dev/null
		sys.stdin = open(os.devnull, 'r')
		sys.stdout = open(os.devnull, 'w')
		sys.stderr = open(os.devnull, 'w')

	def start_detached_process(command):
		script = command ["script"]
	
		# Fork a child process
		pid = os.fork ()
		
		if pid == 0:
			# This is the child process
			# Detach the child process from the parent process
			daemonize ()
			# Execute the command in the child process
			the_process = subprocess.Popen (script, shell = True)
			
			print ("""
			
			
				child process pid:
				
				
				
				""", the_process.pid)
			
			# Exit the child process
			os._exit (0)
		else:
			# This is the parent process
			# Return the PID of the child process
			return pid


	merged_dict = merge ({
		"close_fds": True
	}, Popen_keys)

	print ("merged_dict:", merged_dict)
	print ("packet:", packet)	

	the_process = subprocess.Popen (
		script,
		** merged_dict
	)
	
	return {
		"process_identity": the_process.pid
	}

	#command_to_execute = the_procedure
	detached_process_pid = start_detached_process ({
		"script": " ".join (script)
	})
	
	print ("detached_process_pid:", detached_process_pid)
	
	return {
		"process_identity": detached_process_pid
	}
