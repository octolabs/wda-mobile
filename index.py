
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db
import models

from whoosh import store
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import getdatastoreindex
from whoosh.index import create_in
from whoosh.qparser import QueryParser, MultifieldParser

#SEARCHSCHEMA = Schema(title=TEXT(stored=True))
SEARCHSCHEMA = Schema(title=TEXT(stored=True), content=TEXT,
                path=ID(stored=True), tags=KEYWORD, icon=STORED)


class IndexAPI(webapp.RequestHandler):
    def get(self):
		#ix = getdatastoreindex("hello", schema=SEARCHSCHEMA)
		ix = getdatastoreindex("hello", schema=SEARCHSCHEMA)
		courses=models.Course().all()
		for course in courses:
			writer = ix.writer()
			writer.add_document(title=course.name, content=course.description, path=course.course_id)
			writer.commit()
			#self.response.out.write("indexed %s <br/>" % (course.name))

application = webapp.WSGIApplication(
									[('/api/index', IndexAPI)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()