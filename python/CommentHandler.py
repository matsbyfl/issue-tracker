from google.appengine.ext import webapp
from google.appengine.ext import db
import logging
from lib.models import Issue, Comment
from json import dumps as json
from lib.JSONGenerator import JSONList
from lib.requestUtil import getArgument, htmlCodes

class CommentHandler(webapp.RequestHandler):
	
	@htmlCodes
	def get(self, projectKey, issueKey, key):
		logging.info("get request: "+ str(self.request))
		self.response.out.write( Comment().get(key).toJSON() )
	
	@htmlCodes
	def post(self, projectKey, issueKey, key): #update
		logging.info("post request: "+ str(self.request))
		comment = Comment().get(key)
		comment.Issue = Issue().get(issueKey)
		comment.text = getArgument(self.request, 'text', '"text" is a required field!')
		comment.put()
		url = comment.url(self.request.url)
		self.response.headers.add_header("Location", url)
		self.response.out.write(json(url))
	
	@htmlCodes
	def delete(self, projectKey, issueKey, key):
		logging.info("delete request: "+ str(self.request))
		comment = Comment().get(key)
		comment.delete()
		self.response.out.write(json(str(comment.key())))
