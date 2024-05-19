




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

from ventures import ventures_map
ventures = ventures_map ({
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
			"turn on": {
				"adventure": [ 
					"python3",
					"-m",
					"http.server",
					"8081"
				],
				
				"Popen": {},
				
				"kind": "process_identity"
			}
		}
	]
})

ventures ["turn on"] ()

time.sleep (10)

ventures ["turn off"] ()

```