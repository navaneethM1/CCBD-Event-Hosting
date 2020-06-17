# CCBD-Event-Hosting
A Website to manage the events of CCBD which include the BootCamp, Assignment and Internship Project
# Files
- **static** Folder - It has the main.css file which styles the website.
- **templates** Folder - It has the HTML Files needed.
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
# Building
```sh
$ python ccbd.py
Head over to - http://127.0.0.1:5000/index.html
```
# Technologies Used
1. Flask as a micro web framework - python
2. MongoDB as a backend Database
# Working
The student has to sign-up and create an account. Initially, he can view the attendance details only. On the Admin side, there is a button to fill up the Assignment Topics. After filling the necessary Assignment Topic details and enabling the Assignment View button, the student gets to see the Assignment details on his/her Home Page. Those students who have not attended BootCamp on all the three days will not be able to proceed further with CCBD. Other students can go through the details of Assignment and can form a team of size 2-4, minimum being 2. Various corner cases are handled and taken care of which display appropriate flash messages to inform the student. 3-4 weeks later, the admin enables the Evaluation of Assignment button which enables the teacher of CCBD to start the evaluation process by recording the marks. The next stage is the shortlisting stage wherein the admin can try out different threshold of marks and confirm that criteria which results in the shortlisting of desired number of teams. Once this process is completed, the admin can press on the show results button so that an appropriate message is displayed on the student home page - whether shortlisted or not. Finally, the admin can fill project topic details and then click on assign project topics button which will show the project topic on the shortlisted student page. Lastly, he can enable project evaluation button to evaluate the shortlisted teams' projects.

Besides these features, the admin can also download CSV Files of
- All registered students
- Shortlisted Teams details
- Project Evaluation Details
