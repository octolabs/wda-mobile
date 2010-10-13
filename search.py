import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


from whoosh import store
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser, MultifieldParser
import logging

SEARCHSCHEMA = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))

      
class SearchPage(webapp.RequestHandler):
  def get(self):

	ix = getdatastoreindex("hello", schema=SEARCHSCHEMA)
	parser = QueryParser("content", schema = ix.schema)
	q = parser.parse(self.request.get('query'))
	results = ix.searcher().search(q)

	r=[]
	for result in results:
		rr={"name":result['title'], "id":result['path']}
		r.append(rr)

	template_values = {"results":r}
	path = os.path.join(os.path.dirname(__file__), 'search.html')
	self.response.out.write(template.render(path, template_values))
     


application = webapp.WSGIApplication(
                                     [
                                      ('/search', SearchPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
