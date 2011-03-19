"""A toy-level example of a data model in Google Appengine DB terms.
"""
import logging
from google.appengine.ext import db
from restlet import restutil

class Deone(db.Model):
    data = db.TextProperty()
    
restutil.decorateModuleNamed(__name__)
logging.info('Models in %r decorated', __name__)
