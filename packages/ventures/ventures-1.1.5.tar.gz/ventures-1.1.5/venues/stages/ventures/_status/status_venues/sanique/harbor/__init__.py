

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''


'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	Robyn, rust
		https://robyn.tech/
'''


#++++
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
import json
import os
import traceback
#
#++++

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	env_vars = os.environ.copy ()
	INSPECTOR_PORT = env_vars ['INSPECTOR_PORT']

	print ("""
	
		INSPECTOR_PORT:
		
		""", INSPECTOR_PORT)

	app = Sanic (__name__)
	
	app.extend (config = {
		"oas_url_prefix": "/docs",
		"swagger_ui_configuration": {
			"docExpansion": "list" # "none"
		}
	})
	
	#
	#	https://sanic.dev/en/guide/running/configuration.html#inspector
	#	
	#
	app.config.INSPECTOR = True
	app.config.INSPECTOR_HOST = "0.0.0.0"
	app.config.INSPECTOR_PORT = int (INSPECTOR_PORT)
	
	#
	#	opener
	#
	#
	#app.ext.openapi.add_security_scheme ("api_key", "apiKey")
	app.ext.openapi.add_security_scheme ("api_key", "http")
	


	@app.patch ("/patch_route")
	async def patch_handler(request):
		data = request.json

		return json ({
			"message": "Received PATCH request", 
			"data": data
		})

		
	return app

