import os
import webapp2
import jinja2
import cgi

from game import game, main

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

  def get(self):
    template = JINJA_ENVIRONMENT.get_template('home.html')
    template_values = {"player_types": main.player_types} 
    self.response.write(template.render(template_values))

class SecondPage(webapp2.RequestHandler):

  def post(self):
    self.response.write('<!doctype html><html><body>Running simulation.<pre>')
    numTables = int(cgi.escape(self.request.get('numTables')))
    numOrbits = int(cgi.escape(self.request.get('numOrbits')))
    player_prefs = {}
    for i, player_type in enumerate(main.player_types):
      player_prefs[player_type] = {
        'chosen': bool(cgi.escape(self.request.get(str(player_type))))
      }
      percent = cgi.escape(self.request.get(str(i)))
      if percent:
        player_prefs[player_type]['percent'] = int(percent)
      else:
         player_prefs[player_type]['percent'] = 0
    total_pct = 0
    for prefs in player_prefs.values():
      total_pct += prefs['percent']
    if total_pct != 100:
      print 'error'
      return
    results = main.run(numTables, numOrbits, player_prefs)
    template = JINJA_ENVIRONMENT.get_template('results.html')
    template_values = {'results': results}
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/results', SecondPage),
], debug = True)
