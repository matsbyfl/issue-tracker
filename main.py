import webapp2
from python.Projects import ProjectsHandler
from python.Issues import IssuesHandler

app = webapp2.WSGIApplication([
		('/1/projects/?', ProjectsHandler),
		('/1/projects/([\w\-]+)', ProjectsHandler),
		('/1/projects/([\w\-]+)/issues/?', IssuesHandler),
		('/1/projects/([\w\-]+)/issues/([\w\-]+)', IssuesHandler),
	], debug=True)
