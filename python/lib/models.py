from google.appengine.ext import db
from google.appengine.api import users
import json
	
VERSION = "1"
	
class Project(db.Model):
	name = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	createdBy = db.UserProperty(auto_current_user=True)
	#users = db.StringListProperty()
	#notClosedIssues = db.IntegerProperty(default=0)
	
	def toJSON(self):
		return JSONGenerator(self)
		
	def url(self):
		return "/" + VERSION + makeUrl(self)
	
class Issue(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.UserProperty(auto_current_user_add=True)
	subject = db.StringProperty()
	text = db.StringProperty()
	project = db.ReferenceProperty(Project, collection_name='issues')
	closed = db.BooleanProperty(default=False)
	
	def toJSON(self):
		return JSONGenerator(self)
	
	def url(self):
		return "/" + VERSION + makeUrl(self, self.project)

def makeUrl(obj, parent=None):
	url = "/%ss/%s" % (obj.__class__.__name__.lower(), obj.key())
	if parent:
		url = makeUrl(parent) + url
	return url

def JSONGenerator(obj):
	tempdict = dict([(p, unicode(getattr(obj, p))) for p in obj.properties()])
	tempdict['key'] = unicode(obj.key())
	tempdict['id'] = unicode(obj.key().id())
	jsonString = json.dumps(tempdict).replace('\"True\"', 'true').replace('\"False\"', 'false')
	return jsonString

class EntityNotFoundException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
