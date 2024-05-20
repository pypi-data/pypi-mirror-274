

'''
	_status/monitors/4_detached/status_1.py
'''

'''
	the_procedure = " ".join ([ 
		"python3",
		"-m",
		"http.server",
		"8080",
		"&"
	])

	os.system (the_procedure)
	return;
'''

import os
import sys
import subprocess

def check_1 ():
	the_procedure = " ".join ([ 
		"python3",
		"-m",
		"http.server",
		"14000",
		"&"
	])

	def daemonize():
		# Fork the parent process
		pid = os.fork()
		if pid > 0:
			# Exit the parent process
			sys.exit(0)

		# Detach from the controlling terminal
		os.setsid()

		# Fork again to prevent becoming a session leader
		pid = os.fork()
		if pid > 0:
			# Exit the second parent process
			sys.exit(0)

		# Change the current working directory to root
		os.chdir('/')

		# Set file creation mask
		os.umask(0)

		# Close standard file descriptors
		sys.stdin.close()
		sys.stdout.close()
		sys.stderr.close()

		# Open standard file descriptors to /dev/null
		sys.stdin = open(os.devnull, 'r')
		sys.stdout = open(os.devnull, 'w')
		sys.stderr = open(os.devnull, 'w')

	def start_detached_process(command):
		# Fork a child process
		pid = os.fork()
		if pid == 0:
			# This is the child process
			# Detach the child process from the parent process
			daemonize()
			# Execute the command in the child process
			subprocess.Popen(command, shell=True)
			# Exit the child process
			os._exit(0)
		else:
			# This is the parent process
			# Return the PID of the child process
			return pid


	command_to_execute = the_procedure
	detached_process_pid = start_detached_process(command_to_execute)
	print(f"Detached process started with PID: {detached_process_pid}")

	return;
	
	
checks = {
	'check 1': check_1
}