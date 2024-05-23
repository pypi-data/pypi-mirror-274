
'''
	from vaccines.adventures.sanique.adventure import sanique_adventure
	sanique_adventure ()
'''

from sanique._controls.on import turn_on_sanique
from sanique._controls.off import turn_off_sanique
from sanique._controls.is_on import check_sanique_status
from sanique._controls.refresh import refresh_sanique_status

def sanique_adventure ():
	return {
		"name": "adventure_1_sanique",
		"kind": "task",
		"turn on": {
			"adventure": turn_on_sanique,
		},
		"turn off": turn_off_sanique,
		"is on": check_sanique_status,
		"refresh": refresh_sanique_status
	}