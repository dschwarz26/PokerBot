import os
import webapp2
import jinja2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    	extensions=['jinja2.ext.autoescape'],
    	autoescape=True)

class MainPage(webapp2.RequestHandler):
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('home.html')
        	template_values = {'hi': 'sup'}
		self.response.write(template.render(template_values))

class SecondPage(webapp2.RequestHandler):

	def post(self):
		self.response.write('<!doctype html><html><body>You wrote:<pre>')
       		self.response.write(cgi.escape(self.request.get('content')))
        	self.response.write('</pre></body></html>')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', SecondPage),
], debug = True)
