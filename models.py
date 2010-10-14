from google.appengine.ext import db

class Course(db.Model):
	#content
	#COURSE,COURSE_DESCR_TYPE,EFFDT,DESCRLONG
	course_id = db.StringProperty()
	course_type=db.StringProperty()
	effective_date = db.DateProperty()
	name=db.StringProperty()
	description = db.TextProperty()
	status=db.BooleanProperty()
	min_students=db.IntegerProperty()
	max_students=db.IntegerProperty()
	duration=db.IntegerProperty()
	education_units=db.IntegerProperty()
	mobile_video_url=db.LinkProperty()
	web_video_url=db.LinkProperty()

class Prerequisite(db.Model):
	#prerequisites
	#COURSE,PREREQ_COURSE_CD
	course = db.ReferenceProperty(Course, collection_name="course")
	prerequisite = db.ReferenceProperty(Course, collection_name="prerequisite")

class Session(db.Model):
	#sessions
	#COURSE,SESSION_NBR,COURSE_START_DT,COURSE_END_DT,SESSN_START_TIME,SESSN_END_TIME,MIN_STUDENTS,MAX_STUDENTS
	#dates
	#COURSE,SESSION_NBR,SESSN_START_DT,SESSN_START_TIME,SESSN_END_DT,SESSN_END_TIME,DURATION_TIME,DURATION_UNIT_CD,FACILITY_NAME,ADDRESS1,ADDRESS2,CITY,STATE,SESSN_START_TIME_1,SESSN_END_TIME_1
	course= db.ReferenceProperty(Course)
	session_number=db.StringProperty()
	start_date = db.DateProperty()
	end_date = db.DateProperty()
	start_time = db.TimeProperty()
	end_time = db.TimeProperty()
	min_students=db.IntegerProperty()
	max_students=db.IntegerProperty()
	duration=db.IntegerProperty()
	facility=db.StringProperty()
	address=db.StringProperty()
	address2=db.StringProperty()
	city=db.StringProperty()
	state=db.StringProperty()
	
	
