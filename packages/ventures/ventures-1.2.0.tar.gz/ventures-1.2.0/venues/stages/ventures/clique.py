



'''
	This is for starting sanique in floating (or implicit) mode.
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

def clique ():

	@click.group ("ventures")
	def group ():
		pass


	@group.command ("on")
	def on ():			
		return
		

	@group.command ("off")
	def off ():
		return
		
		
	@group.command ("status")
	def status ():
		return
		

	return group




#



