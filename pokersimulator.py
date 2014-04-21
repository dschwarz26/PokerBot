import os
import webapp2
import jinja2
import cgi

from game import main

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

  def get(self):
    template = JINJA_ENVIRONMENT.get_template('home.html')
    template_values = {} 
    self.response.write(template.render(template_values))

class SecondPage(webapp2.RequestHandler):

  def post(self):
    self.response.write('<!doctype html><html><body>Running simulation.<pre>')
    numTables = int(cgi.escape(self.request.get('numTables')))
    numOrbits = int(cgi.escape(self.request.get('numOrbits')))
    results = main.run(numTables, numOrbits)
    template = JINJA_ENVIRONMENT.get_template('results.html')
    template_values = {'results': results}
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/results', SecondPage),
], debug = True)
