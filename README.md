# CS50 Final Project – Project Management Platform (PMP)
#### Video Demo:  <https://youtu.be/y4hsJLUsqPg>
#### Github Link: <https://github.com/Sirojiddin2021/projectmanagement-platform-ssh>
#### Heroku: <https://projectmanagement-platform.herokuapp.com/>
#### Description:
This project is website based where users can automate their projects and tasks. The website user friendly and simple, where no additional training required. In the beginning, I wanted to create a project like ASANA asana.com to expand my knowledge and learn python programming very deeply and also database management, where I can utilize all my learning during the course .
Technologies used:
-	Flask
-	JS
-	flask_session
-	sqlalchemy
-	werkzeug.security
-	wtforms.validators
-	declarative_base
-	sessionmaker
-	URLSafeTimedSerializer
-	SignatureExpired
-	other small libraries or packages


#How the webpage works?
The idea is simple. The user can register through registration form. During registration user need to provide correct information (email) is important:
-	Username [min=5 symbols, max=50 symbols]
-	Email
-	Password [min=5 symbols, max=80 symbols], before saving to database, password data hashes with generate_password_hash() then stores hashed data into database
-	After registration email confirmation link will be sent to new user and he/she must confirm through confirmation token link. Link expires in one hour.

After the registration, the user will be redirected to fill additional information like,
-	Firstname
-	Lastname
-	Role
-	Rate per/hour
-	About
-	And checkbox need to click if user is project manager


After completing all user will be redirected to home page, where user can see four permanent sections
-	Tasks Due Soon
-	Favorites
-	Recent Projects
-	Default

From navbar user can go to Projects board where user can create, edit, delete - sections, projects, tasks, subtasks.
For each function separate routing function created, where routes


Users cannot access to others tasks or projects. This function will be added next stage where I can complete all other functions like:
-	Create teams
-	Create user messages
-	Create milestones
-	Create companies and branches
-	Create user performances
-	Create task collaborators

#Sessions
Each route checks if the user is authenticated through login page (login_required) function and updates session[“user_id”] parameter to users id. If user closes the page and returns to the same page, website will store that session for a while.
#Routing
In each route there is user id first and section, project, task or subtask id will be added. User cannot change user session so sql injection not possible.
#Database
Database created through “create_engine” if database not exists in the project folder, then it will create new one and fills with required information. To connect with database and commit all queries “sessionmaker” is used. With sqlalchemy all sqlite3 queries become easy and readable. And I figure out that sqlalchemy does not support full join function and currently version limiting with join (INNER JOIN).
#Possible improvements
As I mentioned above this website need to update/improve for the multiusers. Possible improvements:
-	Create teams
-	Create companies
-	Payment option
-	Workhour calculation
-	Manhour calculation
-	User performances
-	Task notifications
-	Link with telegram bots, sms services for notification purposes
-	other

#How to launch application
Requirements table:

	Flask==1.0.2
	itsdangerous==1.1.0
	Jinja2==2.10
	MarkupSafe==1.1.0
	requests==2.7.0
	pyTelegramBotAPI==3.8.2
	Werkzeug==0.14.1
	requests==2.7.0
	datetime
	flask_session==0.4.0
	flask_mail==0.9.1
	flask_wtf==0.15.1
	sqlalchemy==1.4.23
	validators==0.18.2
	email_validator==1.1.3
	gunicorn==19.9.0
    	Click==7.0


1.	This website already running on Heroku. Please follow the link <https://projectmanagement-platform.herokuapp.com/>
2.	If you want to be familiar with code: Please visit my github repository: <https://github.com/Sirojiddin2021/projectmanagement-platform-ssh>
3.	After copying the code, please install all dependencies
4.	Once installed run command flask run
5.	In your browser go to localhost:3000
6.	You are ready to go!


**application.py** - This is main application file that contains major functions like user registration, and also to edit projects, sections, tasks.
1. User registration:
  - *RegForm* > User registration form validator
  - *RequestResetForm* > Send email link to reset password
  - *confirm_email* > Email confirmation (token) function/route
  - *login/logout* > Login and logout functions/routes using session
  - *reset_request* > Password reset (token) function
  - *userinfo* > User additional information
3. *home* > user dashboard page/route
4. *index* > index page or main page
5. *sections* > add new section function/route
  - *delete_section* > delete section function/route
  - *edit_section* > update/edit section function/route
6. *projects* > add new projects funtion/route
  - *delete_project* > delete projects function/route
  - *edit_project* > update/edit project function/route
7. *tasks* > add new task function/route
  - *delete_task* > delete task function/route
  - *edit_task* > update/edit task function/route
8. *subtasks* > add new subtask function/route
  - *delete_subtask* > delete subtask function/route
  - *edit_subtask* > update/edit subtask function/route
9. Error handlers
10. Other files:
**forms.py** contains form validations
**initialization.py** contains database model
**project.db** database file
