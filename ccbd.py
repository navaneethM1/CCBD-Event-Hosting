# required module imports
from flask import Flask, render_template, url_for, request, session, redirect,flash, make_response
from flask_pymongo import PyMongo
import bcrypt

# app setup
app = Flask(__name__)
app.config['MONGO_DBNAME']='CCBD'
app.config['MONGO_URI']='mongodb+srv://Rakshith:rakshith123@cluster0-u7vm7.gcp.mongodb.net/CCBD?retryWrites=true&w=majority'
mongo = PyMongo(app)



#-----------------------------------------------------------------------------#
#-------------------------------Index Page------------------------------------#
#-----------------------------------------------------------------------------#



@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html')



#---------------------------------------------------------------------------------------------------#
#-------------------------------Student and Teacher SignUp,Login------------------------------------#
#---------------------------------------------------------------------------------------------------#



@app.route('/studentLogin', methods=['GET','POST'])
def studentLogin():
	if request.method=='POST':
		users = mongo.db.student
		login_user = users.find_one({'email' : request.form['email']})

		if login_user:
			if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
				session['srn']=login_user['_id']
				return redirect(url_for('home'))
		flash('Incorrect email or password')
	return render_template('studentLogin.html')


@app.route('/teacherLogin', methods=['GET','POST'])
def teacherLogin():
	if request.method=='POST':
		users = mongo.db.faculty
		login_user = users.find_one({'email' : request.form['email']})

		if login_user:
			if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
				session['email']=login_user['email']
				return redirect(url_for('teacher_home'))
		flash('Incorrect email or password')
		return redirect(url_for('teacherLogin'))
	return render_template('teacherLogin.html')


@app.route('/studentSignUp', methods=['POST', 'GET'])
def studentSignUp():
    if request.method == 'POST':
        users = mongo.db.student
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'_id' : request.form['srn'],'department' : request.form['dept'],'firstname' : request.form['firstname'],'lastname' : request.form['lastname'], 'contactnumber' : request.form['contactnumber'],'email' : request.form['email'],'password' : hashpass})
            return redirect(url_for('studentLogin'))
        
        return render_template('studentSignUp.html')

    return render_template('studentSignUp.html')


@app.route('/teacherSignUp', methods=['POST', 'GET'])
def teacherSignUp():
    if request.method == 'POST':
        users = mongo.db.faculty
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'firstname' : request.form['firstname'],'lastname' : request.form['lastname'], 'contactnumber' : request.form['contactnumber'],'email' : request.form['email'],'password' : hashpass})
            return redirect(url_for('teacherLogin'))
        
        return render_template('teacherSignUp.html')

    return render_template('teacherSignUp.html')



#-----------------------------------------------------------------------------#
#-------------------------------Attendance------------------------------------#
#-----------------------------------------------------------------------------#



@app.route('/day1', methods=['POST', 'GET'])
def day1():
	if request.method == 'POST':
		email = request.form['email']
		srn = request.form['srn']
		Student = mongo.db.student.find_one({"_id": srn, "email": email})
		if not Student:
			flash("Incorrect Email or SRN")
			return redirect(url_for('day1'))

		mongo.db.student.update_one({"_id": srn}, {'$set':{'day1': True}})
		flash('Attendance taken Successfully!')

	return render_template('Day1.html')


@app.route('/day2', methods=['POST', 'GET'])
def day2():
	if request.method == 'POST':
		email = request.form['email']
		srn = request.form['srn']
		Student = mongo.db.student.find_one({"_id": srn, "email": email})
		if not Student:
			flash("Incorrect Email or SRN")
			return redirect(url_for('day1'))

		mongo.db.student.update_one({"_id": srn}, {'$set':{'day2': True}})
		flash('Attendance taken Successfully!')

	return render_template('Day2.html')


@app.route('/day3', methods=['POST', 'GET'])
def day3():
	if request.method == 'POST':
		email = request.form['email']
		srn = request.form['srn']
		Student = mongo.db.student.find_one({"_id": srn, "email": email})
		if not Student:
			flash("Incorrect Email or SRN")
			return redirect(url_for('day1'))

		mongo.db.student.update_one({"_id": srn}, {'$set':{'day3': True}})
		flash('Attendance taken Successfully!')

	return render_template('Day3.html')



#--------------------------------------------------------------------------#
#-------------------------------STUDENT------------------------------------#
#--------------------------------------------------------------------------#



@app.route("/home")
def home():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	status=mongo.db.form_status.find_one({'_id':1})
	shortlisted = isShortlisted(session['srn'])
	try:
		allowed=Student['select']
		return render_template('Home.html', Student=Student,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)
	except:
		return render_template('Home.html', Student=Student,status=status['assign_view'],select=None, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)


@app.route("/attendance")
def attendance():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	status=mongo.db.form_status.find_one({'_id':1})
	shortlisted = isShortlisted(session['srn'])
	try:
		allowed=Student['select']
		return render_template('Attendance.html', Student=Student,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)
	except:
		return render_template('Attendance.html', Student=Student,status=status['assign_view'],select=None, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/viewAssignments')
def viewAssignments():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))
	status=mongo.db.form_status.find_one({'_id':1})
	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	shortlisted = isShortlisted(session['srn'])
	assignments = mongo.db.assignment_topics.find({})
	allowed=Student['select']
	return render_template('ViewAssignments.html', Student=Student, assignments=assignments, status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/teamForm', methods=['GET', 'POST'])
def teamForm():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	shortlisted = isShortlisted(session['srn'])
	status=mongo.db.form_status.find_one({'_id':1})
	allowed= Student['select']
	topics = {}
	team_name=''
	for topic in mongo.db.assignment_topics.find({}):
		topics[topic.get('topic')] = topic.get('_id')

	if request.method == 'POST':
		team_srn = [] 
		team_email = []
		s1 = request.form['SRN1']; e1 = request.form['Email1'];
		s2 = request.form['SRN2']; e2 = request.form['Email2'];
		s3 = request.form['SRN3']; e3 = request.form['Email3'];
		s4 = request.form['SRN4']; e4 = request.form['Email4'];
		team_srn.append(s1); team_email.append(e1);
		team_srn.append(s2); team_email.append(e2);
		if s3:
			team_srn.append(s3); team_email.append(e3);
		if s4:
			team_srn.append(s4); team_email.append(e4);

		validity = check_valid(team_srn, team_email)

		if type(validity) == str:
			flash(validity)
			return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)

		if validity:
			# checks if one of the members is the logged in
			if Student['_id'] not in team_srn:
				flash('You should be one of the team members!')
				return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)

			# checks if topic is picked
			try:
				picked_topic = request.form['topic']
			except:
				flash('You did not pick a topic')
				return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)

			picked_topic_id = topics[picked_topic]
			team_srn.sort()
			for srn in team_srn:
				team_name+=srn[-4:]+'_'
			team_name=team_name[:-1]
			mongo.db.student_team.insert({'_id':team_name, 'students': team_srn, 'assignment_topic': picked_topic_id })
			flash('Team Registration Successful!')
			return redirect(url_for('home'))
		
		else:
			flash('Team Registration Unsuccessful. Incorrect SRN or Email')
	
	return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/teamInfo')
def teamInfo():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	team = mongo.db.student_team.find_one(
			{
				'students': session['srn']
			}
		)

	if not team:
		flash('Please form a team and fill in the Team Details')
		return redirect(url_for('teamForm'))

	students_info = []
	for srn in team['students']:
		students_info.append(mongo.db.student.find_one(
				{
					'_id': srn
				}
			)
		)

	topic = mongo.db.assignment_topics.find_one({'_id': team['assignment_topic']})['topic']
	status=mongo.db.form_status.find_one({'_id':1})
	allowed=Student['select']
	shortlisted = isShortlisted(session['srn'])
	return render_template('TeamInfo.html', Student=Student, students_info=students_info, topic=topic,status=status['assign_view'] ,select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=shortlisted)


@app.route("/assgnResults")
def assgnResults():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))
	form_status = mongo.db.form_status.find_one()
	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)

	is_shortlisted = mongo.db.student_team.find_one(
			{
				'students': session['srn']
			}
		)['shortlisted']
	if is_shortlisted:
		flash("1")
		return render_template("AssgnResults.html", Student=Student, status=form_status['assign_view'], select=Student['select'], show_assgn_shortlist_msg=form_status['show_assgn_shortlist_msg'], project_view=form_status['project_view'], shortlisted=is_shortlisted)
	else:
		flash("0")
		return render_template("AssgnResults.html", Student=Student, status=form_status['assign_view'], select=Student['select'], show_assgn_shortlist_msg=form_status['show_assgn_shortlist_msg'], project_view=form_status['project_view'], shortlisted=is_shortlisted)


@app.route('/viewProject')
def viewProject():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	team = mongo.db.student_team.find_one(
			{
				'students': session['srn']
			}
		)
	is_shortlisted = team['shortlisted']
	topic = mongo.db.project_topics.find_one({'_id': team['project']})['topic']
	status=mongo.db.form_status.find_one({'_id':1})
	allowed=Student['select']
	return render_template('ViewProject.html', Student=Student, topic=topic, status=status['assign_view'] ,select=allowed, show_assgn_shortlist_msg=status['show_assgn_shortlist_msg'], project_view=status['project_view'], shortlisted=is_shortlisted)


@app.route('/logout')
def logout():
	session.pop('srn')
	return redirect(url_for('index'))


# helper function
def isShortlisted(srn):
	team = mongo.db.student_team.find_one({'students': srn})
	if not team:
		return False
	try:
		if team['shortlisted']:
			return True
		else:
			return False
	except:
		return False


# helper function
def check_valid(team_srn, team_email):
	for srn, email in zip(team_srn, team_email):
		team = mongo.db.student_team.find_one(
			{
				'students': srn
			}
		)

		# check if student is already in another team
		if team is not None:
			return srn + " already in another team"


		db_s = mongo.db.student.find_one(
			{
				'_id': srn
			}
		)

		if db_s is None:
			return False

		if not db_s['select']:
			return "One of the teammates has not attended Bootcamp on all the 3 days"

		if not (db_s['_id'] == srn and db_s['email'] == email):
			return False

	return True



#--------------------------------------------------------------------------#
#-------------------------------TEACHER------------------------------------#
#--------------------------------------------------------------------------#



@app.route('/teacher_home')
def teacher_home():
	return render_template('teacher_home.html')


@app.route('/bootcamp')
def bootcamp():
	data = mongo.db.student
	query = data.find( {} )
	return render_template('bootcamp.html',query=query) 


@app.route('/assignment', methods=['GET','POST'])
def assignment():
	team=mongo.db.student_team.find({})
	topics=mongo.db.assignment_topics.find({})
	l=group()
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template('assignment.html',topics=topics,team=l,status=status['show_assign_teacher'])


@app.route('/assignment_evaluation/<id1>', methods=['POST','GET'])
def assignment_evaluation(id1):
	if request.method=='POST':
		update= mongo.db.assignment_eval
		update.insert({'_id':request.form['id'],'demo':int(request.form['demo']),'ppt':int(request.form['ppt']),'remarks':request.form['remarks']})
		team=mongo.db.student_team.find_one({'_id':request.form['id']})
		s_i=team['students']
		student=mongo.db.student
		sl=[]
		for i in s_i:
			s=student.find_one({'_id':i})
			sl.append({"fn":s['firstname'],"ln":s['lastname']})
		return render_template("summary_assignment_marks.html",id=request.form['id'], list_names=sl, demo=request.form['demo'],ppt=request.form['ppt'], remarks=request.form['remarks'])
	if mongo.db.assignment_eval.find_one({'_id':id1}):
		flash('This team is already evaluated')
		return redirect(url_for('assignment'))
	return render_template('assignment_evaluation.html',id=id1)


@app.route('/my_func/<id1>')
def my_func(id1):
	return redirect(url_for('assignment_evaluation',id1=id1))


@app.route('/project_evaluation/<id1>', methods=['POST','GET'])
def project_evaluation(id1):
	if request.method=='POST':
		update= mongo.db.project_eval
		update.insert({'_id':request.form['id'],'demo':int(request.form['demo']),'ppt':int(request.form['ppt']),'remarks':request.form['remarks']})
		team=mongo.db.student_team.find_one({'_id':request.form['id']})
		s_i=team['students']
		student=mongo.db.student
		sl=[]
		for i in s_i:
			s=student.find_one({'_id':i})
			sl.append({"fn":s['firstname'],"ln":s['lastname']})
		return render_template("summary_project_marks.html",id=request.form['id'], list_names=sl, demo=request.form['demo'],ppt=request.form['ppt'], remarks=request.form['remarks'])
	if mongo.db.project_eval.find_one({'_id':id1}):
		flash('This team is already evaluated')
		return redirect(url_for('project'))
	return render_template('project_evaluation.html',id=id1)


@app.route('/my_func1/<id1>')
def my_func1(id1):
	return redirect(url_for('project_evaluation',id1=id1))


@app.route('/project')
def project():
	team=mongo.db.student_team.find_one({'shortlisted':True})
	topics=mongo.db.project_topics.find({})
	l=group1()
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template('project.html',topics=topics,team=l,status=status['show_project_assign'])


@app.route('/logout_t')
def logout_t():
    session.pop('email',None)
    return redirect(url_for('index'))


# helper function
def group():
	topics=mongo.db.assignment_topics.find({})
	t_e=mongo.db.student_team.find({})
	ev_team=[]
	for i in mongo.db.assignment_eval.find({}):
		ev_team.append(i['_id'])

	l=[]
	for team in t_e:
		d={}
		d['key']=team['_id']
		d['value']=mongo.db.assignment_topics.find_one({'_id': team['assignment_topic']})['topic']
		if str(team['_id']) in ev_team:
			d['status']="evaluated"
		else:
			d["status"]="Yet To Be Evaluated"
		l.append(d)
	return l


# helper function
def group1():
	topics=mongo.db.project_topics.find({})
	t_e=mongo.db.student_team.find({})
	ev_team=[]
	for i in mongo.db.project_eval.find({}):
		ev_team.append(i['_id'])

	l=[]
	for team in t_e:
		if team['shortlisted']:
			d={}
			d['key']=team['_id']
			d['value']=mongo.db.project_topics.find_one({'_id': team['project']})['topic']
			if str(team['_id']) in ev_team:
				d['status']="evaluated"
			else:
				d["status"]="Yet To Be Evaluated"
			l.append(d)
	return l



#------------------------------------------------------------------------#
#-------------------------------ADMIN------------------------------------#
#------------------------------------------------------------------------#



@app.route('/adminLogin', methods=['GET','POST'])
def adminLogin():
	if request.method=='POST':
		if str(request.form['password'])== "password" and str(request.form['email'])=='admin@gmail.com':
			return redirect(url_for('admin_home'))
	return render_template('adminLogin.html')


@app.route('/admin_home')
def admin_home():
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})
	return render_template("admin_home.html",status=pres['assign_view'], project=pres['show_project_assign'],assign=pres['show_assign_teacher'],project_view=pres['project_view'])


@app.route('/topics_assignment',methods=['GET','POST'])
def topics_assignment():
	if request.method=='POST':
		topic=mongo.db.assignment_topics
		topic.insert({'topic':request.form['topic1'],'desc':request.form['topic1-d']})
		topic.insert({'topic':request.form['topic2'],'desc':request.form['topic2-d']})
		topic.insert({'topic':request.form['topic3'],'desc':request.form['topic3-d']})
		return redirect(url_for('admin_home'))
	return render_template('topics_assignment.html')


@app.route('/form_func')
def form_func():
	if not mongo.db.assignment_topics.find_one({}):
		return redirect(url_for('topics_assignment'))
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['assign_view']
	pres= not pres
	status.update({'_id':1},{'$set':{'assign_view':pres}})

	student=mongo.db.student.find({})
	for i in student:
		if i['day1'] and i['day2'] and i['day3']:
			mongo.db.student.update({'_id':i['_id']},{'$set':{'select':True}})
		else:
			mongo.db.student.update({'_id':i['_id']},{'$set':{'select':False}})

	return redirect(url_for('admin_home'))


@app.route('/form_func2')
def form_func2():
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['show_assign_teacher']
	pres= not pres
	status.update({'_id':1},{'$set':{'show_assign_teacher':pres}})
	return redirect(url_for('admin_home'))


@app.route('/form_func3')
def form_func3():
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['show_project_assign']
	pres= not pres
	status.update({'_id':1},{'$set':{'show_project_assign':pres}})
	return redirect(url_for('admin_home'))


@app.route('/form_func4')
def form_func4():
	if not mongo.db.project_topics.find_one({}):
		return redirect(url_for('topics_projects'))
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['project_view']
	pres= not pres
	status.update({'_id':1},{'$set':{'project_view':pres}})
	return redirect(url_for('admin_home'))


@app.route('/criteria', methods=['GET', 'POST'])
def criteria():
	if request.method == 'POST':
		demo = int(request.form['demo'])
		ppt  = int(request.form['ppt'])
		if 'preview' in request.form:
			no_of_teams_shortlisted = mongo.db.assignment_eval.count_documents({'demo': {'$gte': demo}, 'ppt': {'$gte': ppt}})
			return render_template('Criteria.html', demo=demo, ppt=ppt, no_of_teams_shortlisted=no_of_teams_shortlisted)

		elif 'confirm' in request.form:
			mongo.db.form_status.update_one({}, {'$set': {'show_assgn_shortlist_msg': True}})
			team_ids_shortlisted = []
			for team in mongo.db.assignment_eval.find({'demo': {'$gte': demo}, 'ppt': {'$gte': ppt}}):
				team_ids_shortlisted.append(team['_id'])
			mongo.db.student_team.update_many({}, 
					{
						'$set': {
							'shortlisted': False
						}
					}
				)
			mongo.db.student_team.update_many({'_id': {'$in': team_ids_shortlisted}}, 
					{
						'$set': {
							'shortlisted': True
						}
					}
				)
			return redirect(url_for('admin_home'))

	return render_template('Criteria.html', no_of_teams_shortlisted=-1)


@app.route('/enter_project_topics', methods=['GET', 'POST'])
def enter_project_topics():
	if request.method=='POST':
		status=mongo.db.form_status.find_one({'_id':1})
		number= status['curr_project_num']
		for i in range(1,number+1):
			mongo.db.project_topics.insert({'topic': request.form[str(i)]})
		return redirect(url_for('admin_home'))
	number=mongo.db.student_team.count_documents({'shortlisted':True})
	status=mongo.db.form_status
	status.update({'_id':1},{'$set':{'curr_project_num':number}})
	return render_template('enter_project_topics.html',number=number)


@app.route('/assign_project')
def assign_project():
	topics=mongo.db.project_topics.find({})
	topics_list=[]
	for i in topics:
		topics_list.append(i['_id'])
	teams=mongo.db.student_team
	number=mongo.db.student_team.count_documents({'shortlisted':True})
	
	for i in teams.find({}):
		teams.update_one({'_id':i['_id'],'shortlisted':True},{'$set':{'project':topics_list[number-1]}})
		if i['shortlisted'] and number>0:
			number-=1
	return redirect(url_for('admin_home'))


@app.route('/logout_a')
def logout_a():
    return redirect(url_for('index'))



#----------------------------------------------------------------------#
#-------------------------------CSV------------------------------------#
#----------------------------------------------------------------------#



@app.route("/csv")
def csv():
	csv = "SRN,Name,Department,Phone,Email\n"
	students = mongo.db.student.find({})

	for student in students:
		student_row = student.get("_id") + "," + student.get("firstname").capitalize() + " " + student.get("lastname").capitalize() + "," + student.get("department") + "," + student.get("contactnumber") + "," + student.get("email") + "\n"
		csv += student_row

	response = make_response(csv)
	details = 'attachment; filename=ccbd_registered_students.csv'
	response.headers['Content-Disposition'] = details
	response.mimetype='text/csv'

	return response


@app.route("/csv1")
def csv1():
	csv = "SL No,Project ID,Team Size,Project Title,SRN,Name,Phone,Email\n"
	
	# shortlisted teams
	teams = mongo.db.student_team.find({'shortlisted': True})

	i = 1
	for team in teams:
		students_srn = team.get("students")

		# 1st student row is different from others
		student_zero = mongo.db.student.find_one({"_id": students_srn[0]})
		student_zero_name = student_zero['firstname'].capitalize() + " " + student_zero['lastname'].capitalize()
		assgn_title = mongo.db.assignment_topics.find_one({"_id" : team.get("assignment_topic")})["topic"]
		csv += str(i) + "," + str(team.get("_id")) + "," + str(len(students_srn)) + "," + assgn_title + "," + students_srn[0] + "," + student_zero_name + "," + student_zero["contactnumber"] + "," + student_zero["email"] + "\n"

		# from second student onwards
		for j in range(1, len(students_srn)):
			student = mongo.db.student.find_one({"_id": students_srn[j]})
			student_name = student['firstname'].capitalize() + " " + student['lastname'].capitalize()
			csv += "," * 4 + students_srn[j] + "," + student_name + "," + student["contactnumber"] + "," + student["email"] + "\n"
		i+=1


	response = make_response(csv)
	details = 'attachment; filename=shortlisted_teams.csv'
	response.headers['Content-Disposition'] = details
	response.mimetype='text/csv'

	return response


@app.route("/csv2")
def csv2():
	csv = "Team_Id,Project,Demo Marks,PPT Marks,Total,Remarks\n"
	teams = mongo.db.student_team
	e_v= mongo.db.project_eval.find({})
	topics=mongo.db.project_topics
	for team in e_v:
		t= teams.find_one({'_id':team.get("_id")})
		topic= topics.find_one({'_id':t.get("project")})
		student_row = team.get("_id") + "," + topic['topic'].capitalize() + "," + str(team.get("demo")) + "," + str(team.get("ppt")) + "," + str(team.get("demo")+team.get("ppt"))+","+team.get("remarks")  + "\n"
		csv += student_row

	response = make_response(csv)
	details = 'attachment; filename=ccbd_project_evaluation_results.csv'
	response.headers['Content-Disposition'] = details
	response.mimetype='text/csv'

	return response





# app run
if __name__ == '__main__':
	app.secret_key = 'tTNl~pJog3taI;~q8glvITG/d6cl2tlLUnmbqVs7emCB2{B]6{'
	app.run(debug=True)
