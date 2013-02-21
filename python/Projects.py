from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
import logging
from json import dumps as json
from lib.models import Project, Issue
from lib.JSONGenerator import JSONList

class ProjectsHandler(webapp.RequestHandler):
	def get(self, key=None):
		logging.info("get request: "+ str(self.request))
		if key:
			self.response.out.write(
				Project().get(key).toJSON()
			)
		else:
			self.response.out.write(
				JSONList(
					Project().all()
				)
			)
		
	def post(self, key): #update
		logging.info("post request:"+ str(self.request))
		project = Project().get(key)
		project.name = self.request.get('name')
		project.put()
		self.response.out.write(json(project.url()))
	
	def put(self): #put on server
		logging.info("put request:"+ str(self.request))
		project = Project()
		name = self.request.get('name')
		if not name: raise Exception('"name" can\'t be empty')
		project.name = name
		project.put()
		self.response.out.write(json(project.url()))
		
	def delete(self, key):
		logging.info("delete request:"+ str(self.request))
		keys = [key]
		project = Project().get(key)
		for issue in project.issues:
			keys.append(issue.key())
		logging.info('Deleting: ' + str(keys))
		db.delete(keys)
		self.response.out.write(json.dups(keys))

