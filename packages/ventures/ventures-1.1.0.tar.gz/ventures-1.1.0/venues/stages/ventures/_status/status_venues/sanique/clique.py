

'''
	This is for starting sanique in floating (or implicit) mode.
'''

from vaccines.adventures.sanique._controls.on as turn_on_sanique
from vaccines.adventures.sanique._controls.off as turn_off_sanique
from vaccines.adventures.sanique._controls.sanic.status import check_sanique_status
	
from vaccines._physics import prepare_physics
from vaccines._physics import run_script_from_file
	
import click
import rich

import time
import os
import pathlib
from os.path import dirname, join, normpath
import sys

def clique ():

	@click.group ("sanique")
	def group ():
		pass


	@group.command ("on")
	def on ():			
		turn_on_sanique ()
		

	@group.command ("off")
	def off ():
		turn_off_sanique ()
		
		
	@group.command ("status")
	def status (physics_path):
		check_sanique_status ()
		

	return group




#



