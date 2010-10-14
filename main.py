import os

import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import models

class MainHandler(webapp.RequestHandler):
	def get(self):

		# get categories
		# get subcategories
		
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))		

class CourseHandler(webapp.RequestHandler):
	def get(self):
		q = models.Course.gql("WHERE course_id = :1", self.request.get('course_id'))
		course = q.fetch(1)[0]
		
		q = models.Session.gql("WHERE course_id = :1", course.key())
		sessions = []
		for session in q:
			sessions.append(session)
			
		admin_link = None
		if users.is_current_user_admin():
			admin_link = '/admin/course?course_id=%s' % self.request.get('course_id')
		
		template_values = { 'course': course,
		 					'sessions': sessions,
							'admin_link': admin_link,
							}
		path = os.path.join(os.path.dirname(__file__), 'course.html')
		self.response.out.write(template.render(path, template_values))


class SessionHandler(webapp.RequestHandler):
	def get(self):
		q = models.Session.gql("WHERE session_number = :1", self.request.get('session_number'))
		session = q.fetch(1)[0]
		
		admin_link = None
		if users.is_current_user_admin():
			admin_link = '/admin/session?session_number=%s' % self.request.get('session_number')
			
		template_values = { 'session': session,
							'admin_link': admin_link,
		}
		path = os.path.join(os.path.dirname(__file__), 'session.html')
		self.response.out.write(template.render(path, template_values))		


def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),
		('/course', CourseHandler),
		('/session', SessionHandler),
		],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
