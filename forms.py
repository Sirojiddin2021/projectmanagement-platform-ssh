from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField, DateTimeField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange, InputRequired, EqualTo
from initialization import *    #init, engine, Users
from application import *
#--------- User -----------------------------------------------

# reset password form

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=80)])
    submit = SubmitField('Login')


# for user update
class AddInfo(FlaskForm):
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    phone = StringField('phone')
    role = StringField('role')
    about = StringField('about')
    rate = FloatField('rate')
    pm = BooleanField('pm')


# --------------------------------- Sections -------------------------------------------

# Section Form Class
class SectionAddForm(FlaskForm):
    section_name = StringField('section_name', validators=[DataRequired(), Length(min=1, max=100)])
    section_description = TextAreaField('section_description', validators=[Length(max=200)])

# Section Form Class
class SectionEditForm(FlaskForm):
    e_section_name = StringField('e_section_name', validators=[DataRequired(), Length(min=1, max=100)])
    e_section_description = TextAreaField('e_section_description', validators=[Length(max=200)])

# ---------------------------------- Projects --------------------------------------------

# add project from class
class ProjectAddForm(FlaskForm):
    project_name = StringField('project_name', validators=[DataRequired(), Length(min=1, max=100)])
    project_description = TextAreaField('project_description', validators=[Length(max=200)])
    project_SD = DateField('project_SD', format='%Y-%m-%d', validators=[DataRequired()])
    project_DD = DateField('project_DD', format='%Y-%m-%d', validators=[DataRequired()])
    project_section = IntegerField('project_section', validators=[DataRequired()])

# project from class
class ProjectEditForm(FlaskForm):
    e_project_name = StringField('e_project_name', validators=[DataRequired(), Length(min=1, max=100)])
    e_project_description = TextAreaField('e_project_description', validators=[Length(max=200)])
    e_project_SD = DateField('e_project_SD', format='%Y-%m-%d', validators=[DataRequired()])
    e_project_DD = DateField('e_project_DD', format='%Y-%m-%d', validators=[DataRequired()])
    e_project_section = IntegerField('e_project_section', validators=[DataRequired()])



# --------------------------------- Tasks --------------------------------------------------
# add task from class
class TaskAddForm(FlaskForm):
    task_name = StringField('task_name', validators=[DataRequired(), Length(min=1, max=100)])
    task_description = TextAreaField('task_description', validators=[Length(max=200)])
    task_priority = IntegerField('task_priority')
    task_SD = DateField('task_SD', format='%Y-%m-%d', validators=[DataRequired()])
    task_DD = DateField('task_DD', format='%Y-%m-%d', validators=[DataRequired()])
    task_project = IntegerField('task_project', validators=[DataRequired()])


# edit task from class
class TaskEditForm(FlaskForm):
    e_task_name = StringField('e_task_name', validators=[DataRequired(), Length(min=1, max=100)])
    e_task_description = TextAreaField('e_description', validators=[Length(max=200)])
    e_task_SD = DateTimeField('e_task_SD', format='%Y-%m-%d', validators=[DataRequired()])
    e_task_DD = DateTimeField('e_task_DD', format='%Y-%m-%d', validators=[DataRequired()])
    e_task_project = IntegerField('e_task_project', validators=[DataRequired()])
    e_task_priority = IntegerField('e_task_priority', validators=[DataRequired()])


# --------------------------------- SubTasks --------------------------------------------------
# add subtask from class
class SubtaskAddForm(FlaskForm):
    subtask_name = StringField('subtask_name', validators=[DataRequired(), Length(min=1, max=100)])
    subtask_description = TextAreaField('subtask_description', validators=[Length(max=200)])
    subtask_SD = DateField('subtask_SD', format='%Y-%m-%d', validators=[DataRequired()])
    subtask_DD = DateField('subtask_DD', format='%Y-%m-%d', validators=[DataRequired()])
    subtask_task = IntegerField('subtask_task', validators=[DataRequired()])
    subtask_priority = IntegerField('subtask_priority', validators=[DataRequired()])


# edit subtask from class
class SubtaskEditForm(FlaskForm):
    e_subtask_name = StringField('e_subtask_name', validators=[DataRequired(), Length(min=1, max=5)])
    e_subtask_description = TextAreaField('e_subtask_description', validators=[Length(max=200)])
    e_subtask_SD = DateTimeField('e_subtask_SD', format='%Y-%m-%d', validators=[DataRequired()])
    e_subtask_DD = DateTimeField('e_subtask_DD', format='%Y-%m-%d', validators=[DataRequired()])
    e_subtask_task = IntegerField('e_subtask_task', validators=[DataRequired()])
    e_subtask_priority = IntegerField('e_subtask_priority', validators=[DataRequired()])

