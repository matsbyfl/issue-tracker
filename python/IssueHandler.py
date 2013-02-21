from google.appengine.ext import webapp
from google.appengine.ext import db
import logging
from lib.models import Project, Issue
from json import dumps as json
from lib.JSONGenerator import JSONList
from lib.requestUtil import getArgument, htmlCodes

class IssueHandler(webapp.RequestHandler):
	
	@htmlCodes
	def get(self, projectKey, key):
		logging.info("get request: "+ str(self.request))
		self.response.out.write( Issue().get(key).toJSON() )
	
	@htmlCodes
	def post(self, projectKey, key): #update
		logging.info("post request: "+ str(self.request))
		issue = Issue().get(key)
		issue.project = Project().get(projectKey)
		issue.summary = getArgument(self.request, 'summary', '"summary" is a required field!')
		closed = self.request.get('closed')
		if closed: issue.closed = closed.lower() == "true"
		issue.text = self.request.get('text')
		issue.put()
		url = issue.url(self.request.url)
		self.response.headers.add_header("Location", url)
		self.response.out.write(json(url))
	
	@htmlCodes
	def delete(self, projectKey, key):
		logging.info("delete request: "+ str(self.request))
		issue = Issue().get(key)
		keys = [key]
		for comment in issue.comments:
			keys.append(str(comment.key()))
		logging.info('Deleting: ' + str(keys))
		db.delete(keys)
		self.response.out.write(json(keys))
