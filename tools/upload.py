import csv
import httplib, urllib


courses={}

reader = csv.reader(open("../data/course-detail-description.csv", 'rU'), delimiter=',', quotechar='"')
for row in reader:
	"""
	print row[0]
	print row[1]
	print row[2]
	print row[3].split("\n")[0]
	print row[3]
	"""
	print "---"
	
	courses[row[0]]={"course_id":row[0], "course_type":row[1],
	"effective_date":row[2],
	"name":row[3].split("\n")[0],
	"description":row[3]}

reader = csv.reader(open("../data/course-details.csv", 'rU'), delimiter=',', quotechar='"')
for row in reader:
	"""
	print row[0]
	print row[1]
	print row[2]
	print row[3].split("\n")[0]
	print row[3]
	"""
	print "---"

	courses[row[1]]["min_students"]=row[6].split(".")[0]
	courses[row[1]]["max_students"]=row[7].split(".")[0]
	

for course in courses:
	c=courses[course]
	data={"course_id":c["course_id"],
		"course_type":c["course_type"],
		"effective_date":c["effective_date"],
		"name":c["name"],
		"description":c["description"],
		"max_students":c["max_students"],
		"min_students":c["min_students"],}
		
	print data
	
	params = urllib.urlencode(data)
	conn = httplib.HTTPConnection("localhost:8097")
	conn.request("POST", "/api/course", params)
	response = conn.getresponse()
	print response.status, response.reason

	data = response.read()
	conn.close()

reader = csv.reader(open("../data/courses-prerequisites.csv", 'rU'), delimiter=',', quotechar='"')
for row in reader:
	print row[0]
	print row[1]
	print "---"

	data={"course":row[0],
		"prerequisite":row[1]}

	params = urllib.urlencode(data)
	conn = httplib.HTTPConnection("localhost:8097")
	conn.request("POST", "/api/prerequisite", params)
	response = conn.getresponse()
	print response.status, response.reason

	data = response.read()
	conn.close()	
