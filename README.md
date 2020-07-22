# CCBD-Event-Hosting
A Website to help faculty manage the events of CCBD which include the BootCamp, Assignment and Internship Project *conveniently*
# Files
- **static** Folder - It has the necessary css files which style the website along with the required images.
- **templates** Folder - It has the HTML Files needed.
- *ccbd.py* - The main flask-python script.
# Required packages which needs to be installed
1. Flask
2. bcrypt
3. Flask-PyMongo
4. dnspython
5. bson
```sh
$ pip install Flask
$ pip install bcrypt
$ pip install Flask-PyMongo
$ pip install dnspython
$ pip install bson
```
# Building
```sh
$ python ccbd.py
Head over to - http://127.0.0.1:5000/
```
# Technologies Used
1. Flask as a micro web framework - python
2. MongoDB as a backend Database
3. SMPT for sending Emails for the purpose of password reset
# Working
The student has to sign-up and create an account. Initially, he can view his Profile, about Bootcamp and Timeline. On the Admin side, there is a button to fill up the Assignment Topics. After filling the necessary Assignment Topic details and enabling the Assignment View button, the student gets to see the Assignment details on his/her Home Page. Those students who have not attended BootCamp on all the three days will not be able to proceed further with CCBD and appropriate messages are displayed. Other students can go through the details of Assignment and can form a team of size 2-4, minimum being 2. Various corner cases are handled and taken care of which display appropriate flash messages to inform the student. Provisions for discussion forums wherein students will be able to post questions, and uploading assignment have been included. 3-4 weeks later, the admin enables the Evaluation of Assignment button which enables the teacher of CCBD to start the evaluation process by recording the marks. The next stage is the shortlisting stage wherein the admin can try out different threshold of marks and confirm that criteria which results in the shortlisting of desired number of teams. Once this process is completed, the admin can fill project topic details and then click on the assign project topics button so that an appropriate message is displayed on the student home page - whether shortlisted or not along with project details (if shortlisted). A provision for accepting the internship has also been provided. Lastly, he can enable project evaluation button so that the teachers can evaluate the shortlisted teams' projects.

Besides these features, the admin can also download CSV Files of
- All registered students
- Shortlisted Teams details
- Rejected Teams for Project(teams whose team size went below 2 because of students not accepting)
- Students who did not accept the internship
- Project Evaluation Details
