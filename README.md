# CCBD-Event-Hosting
A Website to manage the events of CCBD which includes the BootCamp, Assignment and Internship Project
# Files
- **Static** Folder - It has the main.css file which styles the website.
- **Templates** Folder - It has the HTML Files needed.
- *ccbd.py* - The main flask-python script.
# Required Packages
1. FLask
2. bcrypt
3. Flask-PyMongo
```sh
$ pip install Flask
$ pip install bcrypt
$ pip install Flask-PyMongo
```
# Working
The student has to sign-up and create an account. Initially, he can view the attendance details only. On the Admin side, there is a button to fill up the Assignment Topics. After filling the necessary Assignment Topic details and enabling the Assignment View button, the student gets to see the Assignment details on his/her Home Page. Those students who have not attended BootCamp on all the three days will not be able to proceed further with CCBD. Other students can go through the details of Assignment and can form a team of size 2-4, minimum being 2. Various corner cases are handled and taken care of which display appropriate flash messages to inform the student. 3-4 weeks later, the admin enables the Evaluation of Assignment button which enables the teacher of CCBD to start the evaluation process by recording the marks. The next stage is the shortlisting stage wherein the admin can try out different threshold of marks and confirm that criteria which results in the shortlisting of desired number of teams. 
