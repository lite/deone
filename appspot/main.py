import wsgiref.handlers
from google.appengine.ext import webapp

from google.appengine.ext.webapp import util

from google.appengine.ext.webapp import template

from suas import session, auth_handlers

# Set up our REST resources
import models

HOME_VIEW = template.Template("""
<head><title>Home</title></head>
<body>
<h3>Demo app for DEONE</h3>
{% if session.flash_msg %}
	<p>{{ session.flash_msg }}</p>
{% endif %}
{% if session.user %}
	<p>Logged in as {{ session.user }}.</p>
	<p><a href="/logout">Log out</a></p>
{% else %}
	<p><a href="/login">Log in</a></p>
	<p><a href="/signup">Sign up</a></p>
{% endif %}
</body>
""")

class HomeHandler(session.RequestHandler):
	def get(self):
		ctx = template.Context({"session": self.session})
		self.response.out.write(HOME_VIEW.render(ctx))

from restlet.intgutil import JsonRestHelper

helper = JsonRestHelper()

class CrudRestHandler(webapp.RequestHandler):
  def __init__(self, *a, **k):
    webapp.RequestHandler.__init__(self, *a, **k)
    helper.hookup(self)
ROUTES = [('/', HomeHandler), ('/(rest)/.*',  CrudRestHandler)] + auth_handlers.ROUTES

#from restlet.handler import CrudRestHandler
#ROUTES = [('/home', HomeHandler), ('/',  CrudRestHandler)] + auth_handlers.ROUTES

def main():
    import logging
    logging.basicConfig(level=logging.DEBUG,)

    # Create the AppEngine WSGI Application
    application = webapp.WSGIApplication(ROUTES, debug=True)

    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
