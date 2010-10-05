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
		course=models.Course()
		course.course_id=self.request.get('course_id')
		course.course_type=self.request.get('course_type')
		#course.effective_date=self.request.get('effective_date')
		course.name=self.request.get('name')
		course.description=self.request.get('description')
		#course.status=self.request.get('status')
		course.min_students=int(self.request.get('min_students'))
		course.max_students=int(self.request.get('max_students'))
		#course.duration=self.request.get('duration')
		#course.education_units=self.request.get('education_units')
		course.put()

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
		session=models.Session()
		session.course=self.request.get('course')
		session.session_number=self.request.get('session_number')
		session.start_date=self.request.get('start_date')
		session.end_date=self.request.get('end_date')
		session.start_time=self.request.get('start_time')
		session.end_time=self.request.get('end_time')
		session.min_students=self.request.get('min_students')
		session.max_students=self.request.get('max_students')
		session.duration=self.request.get('duration')
		session.address=self.request.get('address')
		session.address2=self.request.get('address2')
		session.city=self.request.get('city')
		session.state=self.request.get('state')
		session.put()
		
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