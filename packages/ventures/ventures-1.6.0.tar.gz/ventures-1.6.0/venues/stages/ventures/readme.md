




******

Bravo!  You have received a Medical Diploma from   
the Orbital Convergence University International Air and Water Embassy of the Tangerine Planet.  

You are now officially certified to include this mixer in your practice.

******


# ventures

---

## summary
This is for flipping processes on and off.   
As well it is for checking if processes are on or off.   
		
---		
		
## obtain
```
pip install ventures
```

## tutorial

```
ventures_map_1.py
```
```
import os
import pathlib
from os.path import dirname, join, normpath
import sys
import time

this_folder = pathlib.Path (__file__).parent.resolve ()
the_map = str (
	normpath (join (
		os.getcwd (), 
		"ventures_map.JSON"
	))
)

def turn_on_sanique ():
	return;
	
def turn_off_sanique ():
	return;
	
	
#
#	This needs to return either "on" or "off",
#	"turn on" runs this function to check whether
#	the adventure is "on" or "off.
#
def check_sanique_is_on ():
	return "off"

from ventures import ventures_map
from ventures.clique import ventures_clique

the_ventures = ventures_map ({
	"map": the_map,
	"ventures": [
		{
			"name": "adventure_1",
			"turn on": {
				"adventure": [ 
					"python3",
					"-m",
					"http.server",
					"8080"
				],
				
				"Popen": {},
				
				"kind": "process_identity"
			}
		},
		{
			"name": "adventure_2",
			"kind": "task",
			"turn on": {
				"adventure": turn_on_sanique,
			},
			"turn off": turn_off_sanique,
			"is on": check_sanique_is_on
		}
	]
})
```

## option 1, continued from above
This is the interface to turn on and off ventures
```
the_ventures ["turn on"] ()
the_ventures ["is on"] ()
the_ventures ["turn off"] ()
the_ventures ["turn on"] ({
	"name": "adventure_1"
})
the_ventures ["turn off"] ({
	"name": "adventure_1"
})
the_ventures ["is on"] ()
```

## option 2, continued from above
Ventures has a click interface group that can be 
added to a click interface.
```
import click	
def clique ():
	@click.group ()
	def group ():
		pass

	group.add_command (ventures_clique ({
		"ventures": the_ventures
	}))
	group ()
	
clique ()
```

### The click interface options
Assuming the name of the interface is "voyages".   
```
voyages ventures on
voyages ventures off
voyages ventures status
```

The adventures can be turned on and off by name.   
```
voyages ventures on --name adventure_1
voyages ventures off --name adventure_1
```


## Starting Passive Processes
`#implicit` `#back`
```
from ventures.utilities.hike_passive_forks import hike_passive_forks
hike_passive ({
	"script": [
	
	],
	"Popen": {}
})
```