from google.appengine.ext.db import Model
import json

def JSONList(lst):
	out = []
	for item in lst:
		if isinstance(item, Model):
			out.append(item.toJSON())			
		else:
			out.append(json.dumps(item))
	return "[%s]" % ",".join(out)
