from google.appengine.ext import webapp
from google.appengine.ext import db
import logging
from lib.models import Project, Issue
from json import dumps as json
from lib.JSONGenerator import JSONList

def notEmpty(name, obj):
	if not obj:
		raise Exception('"%s" can\'t be empty' % name)
	

class IssuesHandler(webapp.RequestHandler):
	def get(self, projectKey, key=None):
		logging.info("get request: "+ str(self.request))
		if key:
			self.response.out.write(
				Issue().get(key).toJSON()
			)
		else:
			logging.info('issues: '+ str(Project().get(projectKey).issues))
			self.response.out.write(
				JSONList(
					Project().get(projectKey).issues
				)
			)
		
	def post(self, projectKey, key): #update
		logging.info("post request: "+ str(self.request))
		issue = Issue().get(key)
		project = Project().get(projectKey)
		notEmpty('project', project)
		issue.project = project
		subject = self.request.get('subject')
		notEmpty('subject', subject)
		issue.subject = subject
		issue.text = self.request.get('text')
		issue.put()
		self.response.out.write(json(issue.url()))
	
	def put(self, projectKey): #put on server
		logging.info("put request: "+ str(self.request))
		issue = Issue()
		project = Project().get(projectKey)
		notEmpty('project', project)
		issue.project = project
		subject = self.request.get('subject')
		notEmpty('subject', subject)
		issue.subject = subject
		issue.text = self.request.get('text')
		issue.put()
		self.response.out.write(json(issue.url()))
		
	def delete(self, projectKey, key):
		logging.info("delete request: "+ str(self.request))
		issue = Issue().get(key)
		issue.delete()
		self.response.out.write(json(issue.key()))
