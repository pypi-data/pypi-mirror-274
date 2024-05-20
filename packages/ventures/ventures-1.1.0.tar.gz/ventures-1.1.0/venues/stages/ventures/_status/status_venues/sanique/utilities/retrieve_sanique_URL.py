
'''
	from vaccines.adventures.sanique.utilities.retrieve_sanique_URL import retrieve_sanique_URL
'''

from vaccines._physics import retrieve_physics

def retrieve_sanique_URL ():
	physics = retrieve_physics ()

	return "http://" + physics ["sanique"] ["host"] + ":" + physics ["sanique"] ["port"];