import os

import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, template_values))

class AdminCourseHandler(webapp.RequestHandler):
	def get(self):
		c = Course.gql("WHERE course_id = :1", self.request.get('course_id'))
		template_values = {'course_id':c.course_id,
							'name': c.name,
							'course_type': c.course_type,
							'effective_date': c.effective_date,
							'description': c.description,
							'status': c.status,
							'min_students': c.min_students,
							'max_students': c.max_students,
							'duration': c.duration,
							'education_units': c.education_units,
							'mobile_video_url': c.mobile_video_url,
							'web_video_url': c.web_video_url,
							}
		path = os.path.join(os.path.dirname(__file__), 'admin/admin_course.html')
		self.response.out.write(template.render(path, template_values))


class AdminSessionHandler(webapp.RequestHandler):
	def get(self):
		s = Session.gql("WHERE session_number = :1", self.request.get('session_number'))
		template_values = {'session_number': s.session_number,
							'start_date': s.start_date,
							'end_date': s.end_date,
							'start_time': s.start_time,
							'end_time': s.end_time,
							'min_students': s.min_students,
							'max_students': s.max_students,
							'duration': s.duration,
							'facility': s.facility,
							'address': s.address,
							'address2': s.address2,
							'city': s.city,
							'state': s.state,
							'course_id': s.course.course_id,
							}
		path = os.path.join(os.path.dirname(__file__), 'admin/admin_session.html')
		self.response.out.write(template.render(path, template_values))		


def main():
	application = webapp.WSGIApplication(
		[('/admin', AdminHandler),
		('/admin/course', AdminCourseHandler),
		('/admin/session', AdminSessionHandler),
		],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
