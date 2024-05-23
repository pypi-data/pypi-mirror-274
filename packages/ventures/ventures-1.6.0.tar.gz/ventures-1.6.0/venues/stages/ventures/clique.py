



'''
	This is for starting sanique in floating (or implicit) mode.
'''

'''
	from ventures.clique import ventures_clique
	ventures_clique ({
		"ventures": ventures
	})
'''


#++++
#
import click
import rich
#
#
import time
import os
import pathlib
from os.path import dirname, join, normpath
import sys
#
#++++

def ventures_clique (packet):
	ventures = packet ["ventures"]

	@click.group ("ventures")
	def group ():
		pass


	@group.command ("on")
	@click.option ('--name', help = 'venture name')
	def on (name):		
		if (type (name) == str and len (name) >= 1):
			ventures ["turn on"] ({
				"name": name
			})
			return;
	
		ventures ["turn on"] ()
		

	@group.command ("off")
	@click.option ('--name', help = 'venture name')
	def off (name):
		if (type (name) == str and len (name) >= 1):
			ventures ["turn off"] ({
				"name": name
			})
			return;
	
		ventures ["turn off"] ()
		
		
	@group.command ("refresh")
	@click.option ('--name', help = 'venture name')
	def off (name):
		if (type (name) == str and len (name) >= 1):
			ventures ["turn off"] ({
				"name": name
			})
			ventures ["turn on"] ({
				"name": name
			})
			return;
	
		ventures ["refresh"] ()
		
		
	@group.command ("status")
	@click.option ('--name', help = 'venture name')
	def status (name):
		if (type (name) == str and len (name) >= 1):
			ventures ["is on"] ({
				"name": name
			})
			
		ventures ["is on"] ()
		

	return group

#



