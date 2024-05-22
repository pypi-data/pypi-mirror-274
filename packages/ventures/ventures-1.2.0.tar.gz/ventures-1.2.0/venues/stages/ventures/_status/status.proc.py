

'''
	mongo connection strings
		
		DB: goodest
			
			collection: 
				cautionary_ingredients
				essential_nutrients
'''


import pathlib
from os.path import dirname, join, normpath
import sys
def add_paths_to_system (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))
	

add_paths_to_system ([
	'../../../../stages'
])


#----
#
import biotech
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
import os
import sys
import subprocess
#
#----

#----
#
name = "ventures"
this_directory = pathlib.Path (__file__).parent.resolve ()
venues = str (normpath (join (this_directory, "/habitat/venues")))
this_stage = str (normpath (join (venues, f"stages/{ name }")))

if (len (sys.argv) >= 2):
	glob_string = this_stage + '/' + sys.argv [1]
	db_directory = False
else:
	glob_string = this_stage + '/**/status_*.py'
	db_directory = normpath (join (this_directory, "DB"))

print ("glob string:", glob_string)
#
#----


bio = biotech.on ({
	"glob_string": glob_string,
	
	"simultaneous": True,
	"simultaneous_capacity": 50,

	"time_limit": 60,

	"module_paths": [
		str (normpath (join (this_directory, "status_venues"))),
		str (normpath (join (venues, "stages")))
	],

	"relative_path": this_stage,
	
	"db_directory": db_directory,
	
	"aggregation_format": 2
})


bio ["off"] ()



import time
time.sleep (2)

rich.print_json (data = bio ["proceeds"] ["alarms"])
rich.print_json (data = bio ["proceeds"] ["stats"])


