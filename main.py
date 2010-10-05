import os

import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
	def get(self):

		#query list of routes for dc-circulator
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))		

class RoutesHandler(webapp.RequestHandler):
	def get(self):

		template_values = {'route': "route_tag"}
		path = os.path.join(os.path.dirname(__file__), 'directions.html')
		self.response.out.write(template.render(path, template_values))		


def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),
		('/whereismybus/route/.*', RoutesHandler),
		],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
