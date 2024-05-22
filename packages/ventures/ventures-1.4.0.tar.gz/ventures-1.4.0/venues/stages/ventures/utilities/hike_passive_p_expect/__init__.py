
'''
	from vaccines.mixes.ventures_map.hike_passive_p_expect import hike_passive_p_expect
	hike_passive_p_expect ({
		"script": [
		
		],
		
		"records_path": ""
	})
'''

'''
	objective maybe:
		[ ] start a process that starts a pexpect process,
			that way the pexpect records are logged.
'''

'''
	from biotech.topics.process_on.p_expect import process_on

	env = os.environ.copy ()
	env ["PYTHONPATH"] = ":".join (sys.path)
	the_venture = process_on (
		env = env
	)
	
	the_records = venture ["records"] ()
	for obj in the_queue:
		print ("UTF8:", obj ["UTF8"] ["line"], end = '')
'''

#++++
#
import pexpect
import rich
#
#
import atexit
import os
from multiprocessing import Process, Queue
#
#++++


def hike_passive_p_expect (packet):
	script = packet ["script"]
	script = " ".join (script)

	records_path = packet ["records_path"]

	if ("CWD" not in packet):
		CWD = os.getcwd ()
		
	if ("env" not in packet):
		env = {}
		
	name = "process"
		
	print ("process on?")	
		
	report = {
		"journal": []
	}
	the_process = pexpect.spawn (
		script,
		
		cwd = CWD,
		env = env,
		timeout = None,
		
		logfile = open (logfile_path, 'wb')
		
		# encoding = 'utf-8'
	)
	def awareness_EOF (the_process):
		while not the_process.eof ():
			line = the_process.readline ()

			try:
				UTF8_line = line.decode ('UTF8')
				#UTF8_line = line.decode('ascii')				
				#UTF8_line = line;
				
				UTF8_parsed = "yes"
			except Exception:
				UTF8_line = ""
				UTF8_parsed = "no"
				
			try:
				hexadecimal_line = line.hex ()
				hexadecimal_parsed = "yes"
			except Exception:
				hexadecimal_line = ""
				hexadecimal_parsed = "no"
			
			
			line_parsed = {
				"UTF8": {
					"parsed": UTF8_parsed,
					"line": UTF8_line
				},
				"hexadecimal": {
					"parsed": hexadecimal_parsed,
					"line": hexadecimal_line
				}
			};
			
			
			report ["journal"].append (line_parsed)
			
			if (UTF8_parsed == "yes"):
				print (f'[{ name }]', UTF8_line, end = '')
				
			else:
				print ('unparseable UTF8 line')
			
			# rich.print_json (data = line_parsed)

	print ("process on??")	


	awareness_EOF (the_process)
	#atexit.register (off, p)
	print ("pexpect spawn started?", the_process)
	
	#return {
	#	"process": p,
	#	"report": report
	#}
	
	return {
		"pid": the_process.pid
	}