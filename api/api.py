import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db
import models

class FlushAPI(webapp.RequestHandler):
    def get(self):
		s=models.Session.all()
		db.delete(s)

		p=models.Prerequisite.all()
		db.delete(p)

		c=models.Course.all()
		db.delete(c)


class CourseAPI(webapp.RequestHandler):
    def post(self):
		if not self.request.get('course_id'):
			return
			
		q = models.Course.gql("WHERE course_id = :1", self.request.get('course_id'))
		if q.count() > 0:
			c = q.fetch(1)[0]
		else:
			c = models.Course()
			c.course_id = self.request.get('course_id')
		
		if self.request.get('course_type'):
			c.course_type = self.request.get('course_type')
		#if self.request.get('effective_date'):
		#	c.effective_date = self.request.get('effective_date')
		if self.request.get('name'):
			c.name = self.request.get('name')
		if self.request.get('description'):
			c.description = self.request.get('description')
		#if self.request.get('status'):
		#	c.status = self.request.get('status')
		if self.request.get('min_students'):
			c.min_students=int(self.request.get('min_students'))
		if self.request.get('max_students'):
			c.max_students=int(self.request.get('max_students'))
		#if self.request.get('duration'):
		#	c.duration = self.request.get('duration')
		#if self.request.get('education_units'):
		#	c.education_units = self.request.get('education_units')
		if self.request.get('mobile_video_url'):
			c.mobile_video_url=db.Link(self.request.get('mobile_video_url'))
		if self.request.get('mobile_video_url'):
			c.web_video_url=db.Link(self.request.get('mobile_video_url'))
		
		c.put()

class PrerequisiteAPI(webapp.RequestHandler):
    def post(self):
		pr=models.Prerequisite()
		course=db.GqlQuery("SELECT * FROM Course WHERE course_id = :1", self.request.get('course')).fetch(1)[0]
		prerequisite=db.GqlQuery("SELECT * FROM Course WHERE course_id = :1", self.request.get('prerequisite')).fetch(1)[0]

		pr.course=course
		pr.prerequisite=prerequisite

		pr.put()

class SessionAPI(webapp.RequestHandler):
    def post(self):
		if not self.request.get('session_number'):
			return # Error
			
		q = models.Session.gql("WHERE session_number = :1", self.request.get('session_number'))
		if q.count() > 0:
			s = q.fetch(1)[0]
		else:
			s = models.Session()
			s.session_number = self.request.get('session_number')
		
		if self.request.get('course_id'):
			q = models.Course.gql("WHERE course_id = :1", self.request.get('course_id'))
			if q.count() > 0:
				s.course = self.request.get(q.fetch(1)[0].key())
			else:
				return # Error
		#if self.request.get('start_date'):
		#	s.start_date = self.request.get('start_date')
		#if self.request.get('end_date'):
		#	s.end_date = self.request.get('end_date')
		#if self.request.get('start_time'):
		#	s.start_time = self.request.get('start_time')
		#if self.request.get('end_time'):
		#	s.end_time = self.request.get('end_time')
		if self.request.get('min_students'):
			s.min_students = int(self.request.get('min_students'))
		if self.request.get('max_students'):
			s.max_students = int(self.request.get('max_students'))
		if self.request.get('duration'):
			s.duration = self.request.get('duration')
		if self.request.get('address'):
			s.address = self.request.get('address')
		if self.request.get('address2'):
			s.address2 = self.request.get('address2')
		if self.request.get('city'):
			s.city = self.request.get('city')
		if self.request.get('state'):
			s.state = self.request.get('state')
			
		s.put()
		
application = webapp.WSGIApplication(
									[('/api/flush', FlushAPI),
									('/api/course', CourseAPI),
									('/api/prerequisite', PrerequisiteAPI),
									('/api/session', SessionAPI)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()