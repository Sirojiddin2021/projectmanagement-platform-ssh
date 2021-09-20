# PROJECT MANAGEMENT PLATFORM (PMP) FLASK APPLICATION
#### Video Demo:  <https://youtu.be/82TMmYFpP6I>
#### Description:
This is Project Management website (flask application)
Website works with single user task management, there is no link between users. In the future I would like to multiuser user messages, create teams, assign tasks, exchange files. Furthermore, in addition to above I will add due date notifications, progress bar, users performances and telegram bot notifications!
project.db has future tables that will be used in the future to add more functions.

**app.py** contains below functions:
1. User registration:
  - *RegForm* > User registration form
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
10. Other files:<br>
  - **forms.py** contains form validations
  - **initialization.py** contains database model
  - **project.db** database file
