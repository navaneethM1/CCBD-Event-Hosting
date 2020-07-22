# required module imports
from flask import Flask, render_template, url_for, request, session, redirect,flash, make_response
from flask_pymongo import PyMongo
import bcrypt
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import string 
import random
from bson.objectid import ObjectId


# Static folder
UPLOAD_FOLDER = os.getcwd() + '/static'
ALLOWED_EXTENSIONS = {'jpg'}


# app setup
app = Flask(__name__)
app.config['MONGO_DBNAME']='CCBD'
app.config['MONGO_URI']='mongodb+srv://Rakshith:rakshith123@cluster0-u7vm7.gcp.mongodb.net/CCBD?retryWrites=true&w=majority'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)


# global variable
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#-----------------------------------------------------------------------------#
#-------------------------------Index Page------------------------------------#
#-----------------------------------------------------------------------------#


@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html')


@app.route('/about_ccbd')
def ccbd_info():
	return render_template('About.html')


@app.route('/about_website')
def website():
	return render_template('website.html')



#---------------------------------------------------------------------------------------------------#
#-------------------------------Student and Teacher SignUp,Login------------------------------------#
#---------------------------------------------------------------------------------------------------#



@app.route('/studentLogin', methods=['GET','POST'])
def studentLogin():
	if request.method=='POST':
		users = mongo.db.student
		login_user = users.find_one({'email' : request.form['email']})

		if login_user:
			if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
				session['srn']=login_user['_id']
				return redirect(url_for('profile'))
		flash('Incorrect email or password')
	return render_template('studentLogin.html')


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if 'srn' in session:
		return redirect(url_for('profile'))
	
	if request.method == "POST":
		user = mongo.db.student.find_one({'email':request.form['email']})
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.')
		return redirect(url_for('studentLogin'))
	return render_template('reset_request.html', title='Reset Password')


# sends an email to user
def send_reset_email(user):
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login("rakshithttd23@gmail.com", "Ttd*123456")
	msg = EmailMessage()
	msg['Subject'] = 'Password Reset'
	msg['From'] = "rakshithttd23@gmail.com"
	msg['To'] = user['email']
	N = 10
	res = ''.join(random.choices(string.ascii_uppercase +  string.digits, k = N))
	res = str(res)
	hashed = res.encode('utf-8')
	hashpass = bcrypt.hashpw(hashed, bcrypt.gensalt())
	body = '''
	Please use the below password to login:
	%s
	Once logged in, please change your password in your profile page.
	'''% (res)
	mongo.db.student.update_one({'email':user['email']},{'$set':{'password':hashpass}})
	msg.set_content(body)
	server.send_message(msg)


@app.route('/teacherLogin', methods=['GET','POST'])
def teacherLogin():
	if request.method=='POST':
		users = mongo.db.faculty
		login_user = users.find_one({'email' : request.form['email']})

		if login_user:
			if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
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
        img = request.files['img']
        if img.filename == '':
            flash('Please upload your photo')
            return redirect(url_for('teacherSignUp'))
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'firstname' : request.form['firstname'],'lastname' : request.form['lastname'], 'contactnumber' : request.form['contactnumber'],'email' : request.form['email'],'password' : hashpass})
            if img and allowed_file(img.filename):
            	filename = request.form['firstname'] + request.form['lastname'] + '.jpg'
            	img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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



@app.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	status=mongo.db.form_status.find_one({'_id':1})
	shortlisted = isShortlisted(session['srn'])
	if request.method == 'POST':
		old = request.form['old']
		new = request.form['new']
		if bcrypt.checkpw(old.encode('utf-8'), Student['password']):
			hashpass = bcrypt.hashpw(new.encode('utf-8'), bcrypt.gensalt())
			mongo.db.student.update_one({'_id': session['srn']},{'$set':{'password': hashpass}})
			flash('Password reset successful')
			session.pop('srn')
			return redirect(url_for('studentLogin'))
		else:
			flash('Current password did not match. Try again')
	try:
		allowed=Student['select']
		return render_template('Profile.html', Student=Student,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)
	except:
		return render_template('Profile.html', Student=Student,status=status['assign_view'],select=None,  project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/about')
def about():
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
		return render_template('Student_bootcamp.html', Student=Student,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)
	except:
		return render_template('Student_bootcamp.html', Student=Student,status=status['assign_view'],select=None,  project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/timeline')
def timeline():
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
	status=mongo.db.form_status.find_one({'_id':1})
	one = status['assgn_upload']
	one_date = one.day
	one_month = months[one.month - 1]
	two = one + timedelta(days=2)
	two_date = two.day
	two_month = months[two.month - 1]
	four = status['assgn_deadline']
	four_date = four.day
	four_month = months[four.month - 1]
	three = four - timedelta(days=3)
	three_date = three.day
	three_month = months[three.month - 1]
	five = status['assgn_results']
	five_date = five.day
	five_month = months[five.month - 1]
	six = five + timedelta(days=2)
	six_date = six.day
	six_month = months[six.month - 1]
	allowed=Student['select']
	try:
		team_formed_at = team['team_formed_at']
		team_month = months[team_formed_at.month - 1] # -1 because array is 0 indexed
		team_date = team_formed_at.day
		try:
			submitted_at = team['submitted_at']
			link_month = months[submitted_at.month - 1]
			link_date = submitted_at.day
			try:
				is_accepted = Student['is_accepted']
				accepted_at = Student['accepted_at']
				accepted_month = months[accepted_at.month - 1]
				accepted_date = accepted_at.day
				return render_template('Timeline.html', Student=Student, status=status['assign_view'] ,select=allowed, team_date=team_date, team_month=team_month, link_date=link_date, link_month=link_month, one_date=one_date, one_month=one_month,two_date=two_date, two_month=two_month,three_date=three_date, three_month=three_month,four_date=four_date, four_month=four_month,five_date=five_date, five_month=five_month,six_date=six_date, six_month=six_month, is_accepted=is_accepted, accepted_date=accepted_date, accepted_month=accepted_month)
			except:
				return render_template('Timeline.html', Student=Student, status=status['assign_view'] ,select=allowed, team_date=team_date, team_month=team_month, link_date=link_date, link_month=link_month, one_date=one_date, one_month=one_month,two_date=two_date, two_month=two_month,three_date=three_date, three_month=three_month,four_date=four_date, four_month=four_month,five_date=five_date, five_month=five_month,six_date=six_date, six_month=six_month)
		except:
			return render_template('Timeline.html', Student=Student, status=status['assign_view'] ,select=allowed, team_date=team_date, team_month=team_month, one_date=one_date, one_month=one_month,two_date=two_date, two_month=two_month,three_date=three_date, three_month=three_month,four_date=four_date, four_month=four_month,five_date=five_date, five_month=five_month,six_date=six_date, six_month=six_month)
	except:
		return render_template('Timeline.html', Student=Student, status=status['assign_view'] ,select=allowed, one_date=one_date, one_month=one_month,two_date=two_date, two_month=two_month,three_date=three_date, three_month=three_month,four_date=four_date, four_month=four_month,five_date=five_date, five_month=five_month,six_date=six_date, six_month=six_month)


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
	return render_template('ViewAssignments.html', Student=Student, assignments=assignments, status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/teamForm', methods=['GET', 'POST'])
def teamForm():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	# to redirect to teamInfo Page if he is already in a team
	team = mongo.db.student_team.find_one(
			{
				'students': session['srn']
			}
		)
	if team is not None:
		flash('Team already formed')
		return redirect(url_for('teamInfo'))
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
			return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)

		if validity:
			# checks if one of the members is the logged in
			if Student['_id'] not in team_srn:
				flash('You should be one of the team members!')
				return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)

			# checks if topic is picked
			try:
				picked_topic = request.form['topic']
			except:
				flash('You did not pick a topic')
				return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)

			picked_topic_id = topics[picked_topic]
			team_srn.sort()
			for srn in team_srn:
				team_name+=srn[-4:]+'_'
			team_name=team_name[:-1]
			now = datetime.now()
			mongo.db.student_team.insert({'_id':team_name, 'students': team_srn, 'assignment_topic': picked_topic_id, 'team_formed_at': now})
			flash('Team Registration Successful!')
			return redirect(url_for('teamInfo'))
		
		else:
			flash('Team Registration Unsuccessful. Incorrect SRN or Email')
	one = status['assgn_upload']
	one_date = one.day
	one_month = months[one.month - 1]
	team_form_start = one + timedelta(days=1)
	team_form_end = one + timedelta(days=2)
	now = datetime.now()
	today = datetime(now.year, now.month, now.day)
	if today >= team_form_start and today <= team_form_end:
		return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)
	elif today < team_form_start:
		return redirect(url_for('timeline'))
	else:
		return render_template('Form.html', Student=Student, topics=topics,status=status['assign_view'],select=allowed,  project_view=status['project_view'], shortlisted=shortlisted, crossed=True)


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
	team_name = team['_id']
	for srn in team['students']:
		students_info.append(mongo.db.student.find_one(
				{
					'_id': srn
				}
			)
		)
	topic = mongo.db.assignment_topics.find_one({'_id': team['assignment_topic']})['topic']
	topic = ' '.join(map(str.title, topic.split(' ')))
	status=mongo.db.form_status.find_one({'_id':1})
	allowed=Student['select']
	shortlisted = isShortlisted(session['srn'])
	return render_template('TeamInfo.html', Student=Student, students_info=students_info, team_name=team_name, topic=topic,status=status['assign_view'] ,select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/discussion_forum', methods=['GET', 'POST'])
def discussion_forum():
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
		return redirect(url_for('teamForm'))
	status=mongo.db.form_status.find_one({'_id':1})
	allowed=Student['select']
	if request.method == 'POST':
		query = request.form['query']
		mongo.db.chat.insert({'topic': team['assignment_topic'], 'query': query})
	queries = mongo.db.chat.find({'topic': team['assignment_topic']})
	if queries.count() == 0:
		queries = None
	dates = []
	shortlisted = isShortlisted(session['srn'])
	return render_template('Discussion_forum.html', Student=Student, queries=queries,  status=status['assign_view'] ,select=allowed,  project_view=status['project_view'], shortlisted=shortlisted)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if 'srn' not in session:
		return redirect(url_for('studentLogin'))

	Student = mongo.db.student.find_one(
			{
				'_id': session['srn']
			}
		)
	# take care of teams not formed
	team = mongo.db.student_team.find_one(
			{
				'students': session['srn']
			}
		)
	if team is None:
		return redirect(url_for('teamForm'))

	status=mongo.db.form_status.find_one({'_id':1})
	allowed=Student['select']
	upload_end = status['assgn_deadline']
	upload_start = upload_end - timedelta(days=3)
	now = datetime.now()
	today = datetime(now.year, now.month, now.day)
	if today < upload_start:
		return redirect(url_for('timeline'))
	elif today > upload_end:
			try:
				submitted_at = team['submitted_at']
				link_month = months[submitted_at.month - 1]
				link_date = submitted_at.day
				now = datetime.now()
				time_in_24_str = str(submitted_at.hour) + ':' +  str(submitted_at.minute)
				if(now.day == link_date and now.month == submitted_at.month and now.year == submitted_at.year):
					link_time = 'today' + ' at ' + datetime.strptime(time_in_24_str, "%H:%M").strftime("%I:%M %p")
				else:
					link_time = 'on ' + str(link_date) + '/' + link_month + ' at ' + datetime.strptime(time_in_24_str, "%H:%M").strftime("%I:%M %p")
				return render_template('Upload.html', Student=Student, status=status['assign_view'] ,select=allowed, link_time=link_time, crossed=True)
			except:
				return render_template('Upload.html', Student=Student, status=status['assign_view'] ,select=allowed, crossed=True)
	if request.method == 'POST':
		submission_link = request.form['submission_link']
		team = mongo.db.student_team.update_one(
			{
				'students': session['srn']
			},
			{
				'$set':{'submission_link': submission_link, 'submitted_at': datetime.now()}
			}
		)
		flash('Assignment Submission successfully recorded')
		return render_template('Upload.html', Student=Student, status=status['assign_view'] ,select=allowed)
	try:
		submitted_at = team['submitted_at']
		link_month = months[submitted_at.month - 1]
		link_date = submitted_at.day
		now = datetime.now()
		time_in_24_str = str(submitted_at.hour) + ':' +  str(submitted_at.minute)
		if(now.day == link_date and now.month == submitted_at.month and now.year == submitted_at.year):
			link_time = 'today' + ' at ' + datetime.strptime(time_in_24_str, "%H:%M").strftime("%I:%M %p")
		else:
			link_time = 'on ' + str(link_date) + '/' + link_month + ' at ' + datetime.strptime(time_in_24_str, "%H:%M").strftime("%I:%M %p")
		return render_template('Upload.html', Student=Student, status=status['assign_view'] ,select=allowed, link_time=link_time)
	except:
		return render_template('Upload.html', Student=Student, status=status['assign_view'] ,select=allowed)


@app.route('/viewProject', methods=['GET', 'POST'])
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
	status=mongo.db.form_status.find_one({'_id':1})
	print(status['project_view'])
	allowed=Student['select']
	# take care of teams not formed
	if team is None:
		return redirect(url_for('teamForm'))
	is_shortlisted = team['shortlisted']
	if not is_shortlisted:
		return render_template('ViewProject.html', Student=Student, status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted)
	topic = mongo.db.project_topics.find_one({'_id': team['project']})['topic']
	guide = mongo.db.project_topics.find_one({'_id': team['project']})['guide']
	guide = mongo.db.faculty.find_one({'_id': guide})
	team_name = team['_id']
	accept_start = status['assgn_results']
	accept_end = accept_start + timedelta(days=2)
	now = datetime.now()
	today = datetime(now.year, now.month, now.day)
	if today < accept_start:
		return redirect(url_for('timeline'))
	elif today > accept_end:
		try:
			is_accepted = Student['is_accepted']
			if is_accepted:
				return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='1')
			else:
				return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='0')
		except:
			return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='0', over=True)

	if request.method == 'POST':
		if request.form['accept'] == "yes":
			mongo.db.student.update_one(
			{
				'_id': session['srn']
			},
			{
				'$set': {'is_accepted': True, 'accepted_at': datetime.now()}
			}
		)
			flash('Thank you for taking up this internship! All the very best!')
			return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='1')
		else:
			mongo.db.student.update_one(
			{
				'_id': session['srn']
			},
			{
				'$set': {'is_accepted': False, 'accepted_at': datetime.now()}
			}
		)
			return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='0')
	try:
		is_accepted = Student['is_accepted']
		if is_accepted:
			return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='1')
		else:
			return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, extra='0')
	except:
		five = status['assgn_results']
		five_date = five.day
		five_month = months[five.month - 1]
		six = five + timedelta(days=2)
		six_date = six.day
		six_month = months[six.month - 1]
		return render_template('ViewProject.html', Student=Student, team_name=team_name, topic=topic,guide=guide,status=status['assign_view'] ,select=allowed, project_view=status['project_view'], shortlisted=is_shortlisted, date=six_date, month=six_month)


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
			return srn + " is already in another team"


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
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('teacher_home.html',user_fn=user['firstname'],user_ln=user['lastname'],img_name=img_name,not_ans = count)


@app.route('/bootcamp')
def bootcamp():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	data = mongo.db.student
	query = data.find( {} )
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('bootcamp.html',not_ans = count,query=query,user_fn=user['firstname'],user_ln=user['lastname'],img_name=img_name) 


@app.route('/assignment', methods=['GET','POST'])
def assignment():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	team=mongo.db.student_team.find({})
	topics=mongo.db.assignment_topics.find({})
	l=group()
	status=mongo.db.form_status.find_one({'_id':1})
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('assignment.html',not_ans = count,user_fn=user['firstname'],user_ln=user['lastname'],topics=topics,team=l,status=status['show_assign_teacher'],img_name=img_name)


@app.route('/assignment_evaluation/<id1>', methods=['POST','GET'])
def assignment_evaluation(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	email=session['email']
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
		user=mongo.db.faculty.find_one({'email':email})
		img_name=user['firstname']+user['lastname']+".jpg"
		status=mongo.db.form_status.find_one({'_id':1})
		return render_template("summary_assignment_marks.html",status=status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=request.form['id'], list_names=sl, demo=request.form['demo'],ppt=request.form['ppt'], remarks=request.form['remarks'])
	if mongo.db.assignment_eval.find_one({'_id':id1}):
		flash('This team is already evaluated')
		return redirect(url_for('assignment'))
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template('assignment_evaluation.html',status=status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=id1)


@app.route('/my_func/<id1>')
def my_func(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	status=mongo.db.form_status.find_one({'_id':1})
	return redirect(url_for('assignment_evaluation',status=status['show_assign_teacher'],id1=id1))


@app.route('/project_evaluation/<id1>', methods=['POST','GET'])
def project_evaluation(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	email=session['email']
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
		user=mongo.db.faculty.find_one({'email':email})
		img_name=user['firstname']+user['lastname']+".jpg"
		status=mongo.db.form_status.find_one({'_id':1})
		return render_template("summary_project_marks.html",status=status['show_project_assign'],status_assign = status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=request.form['id'], list_names=sl, demo=request.form['demo'],ppt=request.form['ppt'], remarks=request.form['remarks'])
	if mongo.db.project_eval.find_one({'_id':id1}):
		flash('This team is already evaluated')
		return redirect(url_for('project'))
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template('project_evaluation.html',status=status['show_project_assign'],status_assign = status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=id1)


@app.route('/summary_assignment/<id1>')
def summary_assignment(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	team = mongo.db.assignment_eval.find_one({'_id':id1})
	demo = team['demo']
	ppt = team['ppt']
	remarks = team['remarks']
	team=mongo.db.student_team.find_one({'_id':id1})
	s_i=team['students']
	student=mongo.db.student
	sl=[]
	for i in s_i:
		s=student.find_one({'_id':i})
		sl.append({"fn":s['firstname'],"ln":s['lastname']})
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template("summary_assignment_marks.html",status = status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=id1, list_names=sl, demo=demo,ppt=ppt, remarks=remarks)


@app.route('/summary_project/<id1>')
def summary_project(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	team = mongo.db.project_eval.find_one({'_id':id1})
	demo = team['demo']
	ppt = team['ppt']
	remarks = team['remarks']
	team=mongo.db.student_team.find_one({'_id':id1})
	s_i=team['students']
	student=mongo.db.student
	sl=[]
	for i in s_i:
		s=student.find_one({'_id':i})
		sl.append({"fn":s['firstname'],"ln":s['lastname']})
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	return render_template("summary_project_marks.html",status=status['show_project_assign'],status_assign = status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'],id=id1, list_names=sl, demo=demo,ppt=ppt, remarks=remarks)


@app.route('/my_func1/<id1>')
def my_func1(id1):
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	status=mongo.db.form_status.find_one({'_id':1})
	return redirect(url_for('project_evaluation',id1=id1,status=status['show_project_assign'],status_assign = status['show_assign_teacher'],))


@app.route('/project')
def project():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	team=mongo.db.student_team.find_one({'shortlisted':True})
	topics=mongo.db.project_topics.find({})
	l=group1()
	status=mongo.db.form_status.find_one({'_id':1})
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	user_name=user['firstname']+' '+user['lastname']
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('project.html',not_ans=count,user_name=str(email),user_fn=user['firstname'],user_ln=user['lastname'],topics=topics,team=l,status=status['show_project_assign'],status_assign = status['show_assign_teacher'],img_name=img_name)


@app.route('/logout_t')
def logout_t():
    session.pop('email',None)
    return redirect(url_for('index'))


@app.route('/all_team_details')
def all_teams():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	teams=mongo.db.student_team.find({})
	team_list=[]
	j=1
	for team in teams:
		team_id=team['_id']
		s_i=team['students']
		student=mongo.db.student
		sl=[]
		sid=[]
		for i in s_i:
			s=student.find_one({'_id':i})
			sid.append(i)
			sl.append({"fn":s['firstname'],"ln":s['lastname']})
		assignment_topic= mongo.db.assignment_topics.find_one({'_id':team['assignment_topic']})['topic']
		team_list.append({"slno":j, "id":team_id, "size": len(sl) ,"srns":sid, "names":sl, "title":assignment_topic})
		j+=1
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('assignment_teams.html',not_ans=count,status = status['assign_view'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'], details=team_list)


@app.route('/selected_team_details')
def selected_teams():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	teams=mongo.db.student_team.find({})
	team_list=[]
	j=1
	for team in teams:
		if team['shortlisted']:
			team_id=team['_id']
			s_i=team['students']
			student=mongo.db.student
			sl=[]
			sid=[]
			for i in s_i:
				s=student.find_one({'_id':i})
				sid.append(i)
				sl.append({"fn":s['firstname'],"ln":s['lastname']})
			project_topic=mongo.db.project_topics.find_one({'_id': team['project']})['topic']
			project_guide_id=mongo.db.project_topics.find_one({'_id': team['project']})['guide']
			project_guide_f=mongo.db.faculty.find_one({'_id':project_guide_id})
			project_guide=project_guide_f['firstname']+' '+project_guide_f['lastname']
			team_list.append({"slno":j, "id":team_id, "size": len(sl) ,"srns":sid, "names":sl, "title":project_topic,"guide":project_guide})
			j+=1
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	status=mongo.db.form_status.find_one({'_id':1})
	count = mongo.db.chat.count_documents({"answer":None})
	return render_template('project_teams.html',not_ans = count,status=status['project_view'],status_assign = status['show_assign_teacher'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'], details=team_list)


@app.route('/show_queries',methods=["POST","GET"])
def show_queries():
	if 'email' not in session:
		return redirect(url_for('teacherLogin'))
	if request.method == "POST":
		query_id = request.form['id']
		answer = request.form['reply']
		timestamp = datetime.now()
		email = session['email']
		teacher = mongo.db.faculty.find_one({'email':email})
		name = teacher['firstname']+' '+teacher['lastname']
		mongo.db.chat.update_one({'_id':ObjectId(query_id)},{'$set':{'teacher':name,'answer': answer,'timestamp':timestamp}})
		return redirect(url_for('show_queries'))


	all_queries = mongo.db.chat.find({})
	details = []
	i = 0
	for query in all_queries:
		topic = mongo.db.assignment_topics.find_one({'_id':query['topic']})['topic']
		d = {}
		d['query_id'] = query['_id']
		d['topic'] = topic
		d['query'] = query['query']
		try :
			d['answer'] = query['answer']
			d['time'] = query['timestamp'].strftime("%X")
			d['date'] = query['timestamp'].strftime("%x")
		except:
			d['answer'] = False
			i += 1
		details.append(d)
	email=session['email']
	user=mongo.db.faculty.find_one({'email':email})
	img_name=user['firstname']+user['lastname']+".jpg"
	user_name=user['firstname']+' '+user['lastname']
	status=mongo.db.form_status.find_one({'_id':1})
	if i == 0:
		return render_template('teacher_reply_query.html', status = status['assign_view'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'], details = details)
	return render_template('teacher_reply_query.html', not_ans = i,status = status['assign_view'],img_name=img_name,user_fn=user['firstname'],user_ln=user['lastname'], details = details)
	

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
		s_i=team['students']
		student=mongo.db.student
		sl=[]
		for i in s_i:
			s=student.find_one({'_id':i})
			sl.append({"fn":s['firstname'],"ln":s['lastname']})
		d['name_list']=sl
		d['value']=mongo.db.assignment_topics.find_one({'_id': team['assignment_topic']})['topic']
		try :
			d['link']=team['submission_link']
		except:
			d['link']="no"
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
			s_i=team['students']
			student=mongo.db.student
			sl=[]
			for i in s_i:
				s=student.find_one({'_id':i})
				sl.append({"fn":s['firstname'],"ln":s['lastname']})
			d['name_list']=sl
			assignment_topic= mongo.db.assignment_topics.find_one({'_id':team['assignment_topic']})['topic']
			d['assign']=assignment_topic
			d['value']=mongo.db.project_topics.find_one({'_id': team['project']})['topic']
			project_guide_id=mongo.db.project_topics.find_one({'_id': team['project']})['guide']
			project_guide_f=mongo.db.faculty.find_one({'_id':project_guide_id})
			project_guide=project_guide_f['firstname']+' '+project_guide_f['lastname']
			d['guide']=project_guide
			d['email']=project_guide_f['email']
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
			session['admin'] = True
			return redirect(url_for('admin_home'))
	return render_template('adminLogin.html')


@app.route('/admin_home', methods=['GET','POST'])
def admin_home():
	if 'admin' not in session:
		return redirect('adminLogin')
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})
	if request.method=='POST':
		assgn_upload = datetime(int(request.form['assgn_upload'].split('-')[0]),int(request.form['assgn_upload'].split('-')[1]),int(request.form['assgn_upload'].split('-')[2]))
		assgn_deadline = datetime(int(request.form['assgn_deadline'].split('-')[0]),int(request.form['assgn_deadline'].split('-')[1]),int(request.form['assgn_deadline'].split('-')[2]))
		assgn_results = datetime(int(request.form['assgn_results'].split('-')[0]),int(request.form['assgn_results'].split('-')[1]),int(request.form['assgn_results'].split('-')[2]))
		status.update({'_id':1},{'$set':{'assgn_upload': assgn_upload,'assgn_deadline': assgn_deadline,'assgn_results': assgn_results}})
		return render_template("admin_home.html",status=pres['assign_view'], project=pres['show_project_assign'],assign=pres['show_assign_teacher'],project_view=pres['project_view'], assgn_upload=assgn_upload, assgn_deadline=assgn_deadline, assgn_results=assgn_results)
	try:
		return render_template("admin_home.html",status=pres['assign_view'], project=pres['show_project_assign'],assign=pres['show_assign_teacher'],project_view=pres['project_view'], assgn_upload=pres['assgn_upload'], assgn_deadline=pres['assgn_deadline'], assgn_results=pres['assgn_results'])
	except:
		return render_template("admin_home.html",status=pres['assign_view'], project=pres['show_project_assign'],assign=pres['show_assign_teacher'],project_view=pres['project_view'])


@app.route('/topics_assignment',methods=['GET','POST'])
def topics_assignment():
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method=='POST':
		topic=mongo.db.assignment_topics
		topic.insert({'topic':request.form['topic1'],'desc':request.form['topic1-d']})
		topic.insert({'topic':request.form['topic2'],'desc':request.form['topic2-d']})
		topic.insert({'topic':request.form['topic3'],'desc':request.form['topic3-d']})
		return redirect(url_for('admin_data'))
	return render_template('topics_assignment.html')


@app.route('/form_func')
def form_func():
	if 'admin' not in session:
		return redirect('adminLogin')
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
	if 'admin' not in session:
		return redirect('adminLogin')
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['show_assign_teacher']
	pres= not pres
	status.update({'_id':1},{'$set':{'show_assign_teacher':pres}})
	return redirect(url_for('admin_home'))


@app.route('/form_func3')
def form_func3():
	if 'admin' not in session:
		return redirect('adminLogin')
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['show_project_assign']
	pres= not pres
	status.update({'_id':1},{'$set':{'show_project_assign':pres}})
	return redirect(url_for('admin_home'))


@app.route('/form_func4')
def form_func4():
	if 'admin' not in session:
		return redirect('adminLogin')
	if not mongo.db.project_topics.find_one({}):
		return redirect(url_for('topics_projects'))
	status=mongo.db.form_status
	pres=status.find_one({'_id':1})['project_view']
	pres= not pres
	status.update({'_id':1},{'$set':{'project_view':pres}})
	return redirect(url_for('admin_home'))


@app.route('/criteria', methods=['GET', 'POST'])
def criteria():
	if 'admin' not in session:
		return redirect('adminLogin')
	total_no_teams = mongo.db.student_team.count_documents({})
	if request.method == 'POST':
		demo = int(request.form['demo'])
		ppt  = int(request.form['ppt'])
		if 'preview' in request.form:
			no_of_teams_shortlisted = mongo.db.assignment_eval.count_documents({'demo': {'$gte': demo}, 'ppt': {'$gte': ppt}})
			return render_template('Criteria.html', demo=demo, ppt=ppt, no_of_teams_shortlisted=no_of_teams_shortlisted, total_no_teams=total_no_teams)

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
			return redirect(url_for('admin_data'))

	return render_template('Criteria.html', no_of_teams_shortlisted=-1, total_no_teams=total_no_teams)


@app.route('/enter_project_topics', methods=['GET', 'POST'])
def enter_project_topics():
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method=='POST':
		status=mongo.db.form_status.find_one({'_id':1})
		number= status['curr_project_num']
		for i in range(1,number+1):
			guide=request.form[str(str(i)+'-teacher')]
			faculty=mongo.db.faculty.find({})
			for teacher in faculty:
				if (teacher['firstname']+' '+teacher['lastname'])==guide:
					mongo.db.project_topics.insert({'topic': request.form[str(i)], 'guide': teacher['_id']})
		return redirect(url_for('admin_data'))
	number=mongo.db.student_team.count_documents({'shortlisted':True})
	status=mongo.db.form_status
	status.update({'_id':1},{'$set':{'curr_project_num':number}})
	faculty=mongo.db.faculty.find({})
	fl=[]
	for teacher in faculty:
		fl.append({'key1':teacher['firstname'],'key2':teacher['lastname']})
	return render_template('enter_project_topics.html',number=number,faculty=fl)


@app.route('/assign_project')
def assign_project():
	if 'admin' not in session:
		return redirect('adminLogin')
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
	return redirect(url_for('admin_data'))


@app.route('/confirming_project')
def confirming_project():
	if 'admin' not in session:
		return redirect('adminLogin')
	results = mongo.db.form_status.find_one({'_id':1})['assgn_results']
	deadline = results + timedelta(days = 2)
	if date.today() > deadline:
		teams = mongo.db.student_team.find({'shortlisted':True})
		for team in teams:
			students = team['students']
			count = 0
			for i in students:
				student = mongo.db.student.find_one({'_id':i})
				try:
					if not student['is_accepted'] :
						mongo.db.reject_data.insert({'_id':i, 'team_id':team['_id']})
						mongo.db.student_team.update( { '_id': team['_id'] }, { '$pull': {  students: { [i] } } } )
					else:
						count+=1
				except:
					mongo.db.reject_data.insert({'_id':i, 'team_id':team['_id']})
					mongo.db.student_team.update( { '_id': team['_id'] }, { '$pull': {  students: { [i] } } } )
				
			if count<2:
				mongo.db.student_team.update_one({"_id": team['_id']}, {'$set':{'rejected': True}})
			else :
				mongo.db.student_team.update_one({"_id": team['_id']}, {'$set':{'rejected': False}})
				team_srn = students
				team_srn.sort()
				for srn in team_srn:
					team_name+=srn[-4:]+'_'
				team_name=team_name[:-1]
				mongo.db.student_team.update_one({"_id": team['_id']}, {'$set':{'_id': team_name}})
	return redirect(url_for('admin_data'))


@app.route('/modify')
def modify():
	if 'admin' not in session:
		return redirect('adminLogin')
	return render_template('modify.html')


@app.route('/modify_student_srn', methods=['GET', 'POST'])
def modify_student_srn():
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method == "POST":
		return redirect(url_for('modify_student',srn=request.form['srn']))
	return render_template('srn.html')


@app.route('/modify_student/<srn>',methods=['GET','POST'])
def modify_student(srn):
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method == "POST":
		srn = request.form['srn']
		student = mongo.db.student.find_one({'_id':srn})
		
		mongo.db.student.update_one({'_id':srn},{'$set':{'firstname':request.form['firstname']}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'lastname':request.form['lastname']}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'department':request.form['department']}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'contactnumber':request.form['contactnumber']}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'email':request.form['email']}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'day1':bool(request.form['day1'])}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'day2':bool(request.form['day2'])}})
		mongo.db.student.update_one({'_id':srn},{'$set':{'day3':bool(request.form['day3'])}})
		
		return redirect(url_for('modify'))


	
	student = mongo.db.student.find_one({'_id':srn})
	details = {'id':srn,'department':student['department'],'email': student['email'],'day3': student['day3'],'day2': student['day2'],'day1': student['day1'],'firstname': student['firstname'],'lastname': student['lastname'],'contactnumber': student['contactnumber']}
	
	return render_template('modify_student.html',details = details)


@app.route('/admin_data')
def admin_data():
	if 'admin' not in session:
		return redirect('adminLogin')
	return render_template('admin_data.html')


@app.route('/csv_files')
def csv_files():
	if 'admin' not in session:
		return redirect('adminLogin')
	return render_template("csv_files.html")


@app.route('/faculty_email',methods=['GET','POST'])
def faculty_email():
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method == "POST":
		return redirect(url_for('modify_faculty',email=request.form['email']))
	return render_template('email.html')


@app.route('/faculty_password',methods=['GET','POST'])
def faculty_password():
	if request.method == 'POST':
		users = mongo.db.faculty
		existing_user = users.find_one({'email' : request.form['email']})
		if existing_user:
			hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
			users.update_one({'email':request.form['email']},{'$set':{'password':hashpass}})
			return redirect(url_for('modify'))
	return render_template('faculty_password.html')


@app.route('/modify_faculty/<email>', methods=['GET','POST'])
def modify_faculty(email):
	if 'admin' not in session:
		return redirect('adminLogin')
	if request.method == "POST":
		email = request.form['email']
		mongo.db.faculty.update_one({'email': email},{'$set':{'firstname':request.form['firstname']}})
		mongo.db.faculty.update_one({'email': email},{'$set':{'lastname':request.form['lastname']}})
		mongo.db.faculty.update_one({'email': email},{'$set':{'contactnumber':request.form['contactnumber']}})
		return redirect(url_for('modify'))
	teacher = mongo.db.faculty.find_one({'email':email})
	details = {'email':email,'firstname': teacher['firstname'],'lastname': teacher['lastname'],'contactnumber':teacher['contactnumber']}
	return render_template('modify_faculty.html',details=details)


@app.route('/logout_a')
def logout_a():
	session.pop('admin')
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


@app.route('/csv3')
def csv3():
	csv = "SL No,Project ID,Team Size,SRN,Name,Phone,Email\n"
	
	# shortlisted teams
	teams = mongo.db.student_team.find({'$and':[{'shortlisted': True},{'rejected':True}]})
	try :
		i = 1
		for team in teams:
			students_srn =team.get("students")
			students= mongo.db.reject_data.find({'team_id':team['_id']})
			for student in students:
				students_srn.append(student['_id'])

			# 1st student row is different from others
			student_zero = mongo.db.student.find_one({"_id": students_srn[0]})
			student_zero_name = student_zero['firstname'].capitalize() + " " + student_zero['lastname'].capitalize()
			csv += str(i) + "," + str(team.get("_id")) + "," + str(len(students_srn)) + "," + "," + students_srn[0] + "," + student_zero_name + "," + student_zero["contactnumber"] + "," + student_zero["email"] + "\n"

			# from second student onwards
			for j in range(1, len(students_srn)):
				student = mongo.db.student.find_one({"_id": students_srn[j]})
				student_name = student['firstname'].capitalize() + " " + student['lastname'].capitalize()
				csv += "," * 4 + students_srn[j] + "," + student_name + "," + student["contactnumber"] + "," + student["email"] + "\n"
			i+=1
	except:
		pass

	response = make_response(csv)
	details = 'attachment; filename=Teams_Rejected_Due_To_Insufficient_Size.csv'
	response.headers['Content-Disposition'] = details
	response.mimetype='text/csv'

	return response


@app.route('/csv4')
def csv4():
	csv = "SL No,Project ID,SRN,Name,Phone,Email\n"
	students = mongo.db.reject_data.find({})
	j=1
	for i in students :
		student = mongo.db.student.find_one({'_id':i['_id']})
		name = student['firstname'].capitalize() + " " + student['lastname'].capitalize()
		csv += str(j) + "," + i['team_id'] + "," + i["_id"] + "," + name +  student["contactnumber"] + "," + student["email"] + "\n"
		i+=1

	response = make_response(csv)
	details = 'attachment; filename=Students_Who_Have_Not_Accepted_The_Internship.csv'
	response.headers['Content-Disposition'] = details
	response.mimetype='text/csv'

	return response




# app run
if __name__ == '__main__':
	app.secret_key = 'tTNl~pJog3taI;~q8glvITG/d6cl2tlLUnmbqVs7emCB2{B]6{'
	app.run(debug=True)
