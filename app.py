import os
#import validators

#from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from flask_wtf.csrf import CSRFProtect

from initialization import *    #init, engine, Users

from forms import *   #RegForm, LoginForm, AddInfo
from wtforms.validators import ValidationError

from sqlalchemy.sql import text, column
from sqlalchemy import update, or_

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from helpers import apology, login_required, usd

# to get current date and time
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
#app.config["TEMPLATES_AUTO_RELOAD"] = True
#app.config['SECRET_KEY'] = 'any secret string'

# Ensure responses aren't cached
"""
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
"""

# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'Thisissecret'
CSRFProtect(app)
Session(app)


SessionDB=sessionmaker(bind=engine)
dbsession = SessionDB()


#--------------------------------------------------------- Forms (User registration form)  -------------------------------------------------------#
class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = dbsession.query(Users).filter(Users.Username==username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = dbsession.query(Users).filter(Users.Email==email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')


#--------------------------------------------------------- Forms (User request password reset form)  ---------------------------------------------#
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

    def validate_email(self, email):
        user = dbsession.query(Users).filter(Users.Email==email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')





#--------------------------------------------------------- User email confirmation  --------------------------------------------------------------#

app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisissecret')

@app.route('/<string:Id>/confirm/<string:token>')
def confirm_email(Id, token):
    try:
        s.loads(token, salt='email-confirm', max_age=3600) # one hour or 3600 seconds
    except SignatureExpired:
        flash("The token is expired")
    # update users table
    user = dbsession.query(Users).filter(Users.Id==Id).first()
    if user:
        user.IsConfirmed = True
        dbsession.commit()
        flash("Email has confirmed")
    return redirect("/{}/home".format(user.Id))

@app.route("/temp", methods=["GET", "POST"])
@login_required
def tempo():
    return render_template("temper.html")

#------------------------------------------------------------Login and Logout--------------------------------------------------------------------#

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    form = LoginForm()
    if form.validate_on_submit():

        user = dbsession.query(Users).filter(or_(Users.Username==form.username.data, Users.Email==form.username.data)).first()
        if user:
            if check_password_hash(user.Password, form.password.data):
                session["user_id"] = user.Id
                return redirect("/{}/home".format(user.Id))
            else:
                return render_template("user/login.html", form=form, password_not_matches=True)
        else:
            return render_template("user/login.html", form=form, username_not_matches=True)

    return render_template("user/login.html", form=form)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#----------------------------------------------------------------------Reset password--------------------------------------------------------
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

    form = RequestResetForm()
    if form.validate_on_submit():
        user = dbsession.query(Users).filter(Users.Email==form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)


@app.route("/<string:Id>/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(Id,token):
    try:
        s.loads(token, salt='reset-password', max_age=3600)
    except:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    user = dbsession.query(Users).filter(Users.Id==Id).first()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.Password = generate_password_hash(form.password.data)
        dbsession.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)


def send_reset_email(user):
    token = s.dumps(user.Email, salt='reset-password')
    msg = Message('Password Reset Request', sender='sirojiddin.shodiev@gmail.com', recipients=[user.Email])
    link = url_for('reset_token', Id=user.Id, token=token, _external=True)
    msg.body = 'To reset your password, visit the following link: {}'.format(link)
    mail.send(msg)


#----------------------------------------------------------------Registration----------------------------------------------------------------

# user registration function
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    form = RegForm()
    if form.validate_on_submit():

        username = dbsession.query(Users).filter(Users.Username==form.username.data).first()
        email = dbsession.query(Users).filter(Users.Email==form.email.data).first()

        if not username and not email:

            user = Users(
                Username = form.username.data,
                Password = generate_password_hash(form.password.data),
                Email = form.email.data,
                IsConfirmed = False
                )

            dbsession.add(user)
            dbsession.commit()
            query = dbsession.query(Users.Id).filter_by(Username=form.username.data).first()
            session["user_id"] = query.Id
            flash('A confirmation email has been sent via email.', 'success')

            # send confirmation email
            token = s.dumps(user.Email, salt='email-confirm')
            msg = Message('Please confirm your email', sender='sirojiddin.shodiev@gmail.com', recipients=[user.Email])
            link = url_for('confirm_email', Id=query.Id, token=token, _external=True)
            msg.body = 'Welcome! Thanks for signing up. Please follow this link to activate your account {}'.format(link)
            mail.send(msg)

            return redirect("/{}/userinfo".format(query.Id))
        return render_template("/user/register.html", form=form)


    return render_template("/user/register.html", form=form)


#---------------------------------------------------------------------------------------User update information---------------------------------
@app.route("/<string:Id>/userinfo", methods=["GET", "POST"])
@login_required
def userinfo(Id):
    """ User update function """

    form = AddInfo()
    user = dbsession.query(Users).filter(Users.Id==Id).first()
    roles = dbsession.query(Roles).all()

    if form.validate_on_submit():

        user.Firstname = form.firstname.data
        user.Lastname = form.lastname.data
        user.Role = form.role.data
        user.Phone = form.phone.data
        user.Rate = form.rate.data
        user.About = form.about.data
        user.Project_manager = form.pm.data
        dbsession.commit()
        session["user_id"] = user.Id
        return redirect("/{}/home".format(user.Id))

    return render_template("/user/info.html", form=form, userdata=user, roles=roles)

#----------------------------------------------------------------------------------------Dashboard--------------------------------------------------
@app.route("/<string:Id>/home", methods=["GET", "POST"])
@login_required
def home(Id):
    """ home page """
    all_sections = dbsession.query(Sections).filter(or_(Sections.UserID==Id)|(Sections.Permanent==True)).all()
    all_projects = dbsession.query(Projects.Name, Projects.Description, Projects.SD, Projects.DD, Sections.Name.label("Section_name"), Sections.Id.label("Section_ID"), Users.Username.label("Username")).join(Sections, Sections.Id==Projects.SectionID).join(Users,Users.Id==Id).where(Projects.UserID==Id).all()
    return render_template("user/home.html", usersections=all_sections, userprojects=all_projects)

#--------------------------------------------------------------------------------------- Home page -------------------------------------------------#
@app.route("/")
def index():
    """initialization"""
    init()
    query = dbsession.query(Sections).filter(or_(Sections.Name == "Tasks Due Soon")|(Sections.Name == "Favorites")|(Sections.Name == "Recent Projects")).all()
    if not query:
        sections=[
            Sections(Name='Tasks Due Soon', Description='All due date close tasks', Permanent=True),
            Sections(Name='Favorites', Description='All favorite tasks', Permanent=True),
            Sections(Name='Recent Projects', Description='All recent added projects', Permanent=True),
            Sections(Name='Default', Description='All unsectioned projects', Permanent=True)
            ]

        dbsession.add_all(sections)
        priorities=[
            Priorities(Name='Very Low'),
            Priorities(Name='Low'),
            Priorities(Name='Medium'),
            Priorities(Name='High'),
            Priorities(Name='Very High')
            ]
        dbsession.add_all(priorities)

        roles=[
            Roles(Name='Administrative Assistant'),
            Roles(Name='Receptionist'),
            Roles(Name='Office Manager'),
            Roles(Name='Auditing Clerk'),
            Roles(Name='Bookkeeper'),
            Roles(Name='Account Executive'),
            Roles(Name='Branch Manager'),
            Roles(Name='Business Manager'),
            Roles(Name='Quality Control Coordinator'),
            Roles(Name='Administrative Manager'),
            Roles(Name='Chief Executive Officer'),
            Roles(Name='Business Analyst'),
            Roles(Name='Risk Manager'),
            Roles(Name='Human Resources'),
            Roles(Name='Office Assistant'),
            Roles(Name='Secretary'),
            Roles(Name='Office Clerk'),
            Roles(Name='File Clerk'),
            Roles(Name='Account Collector'),
            Roles(Name='Administrative Specialist'),
            Roles(Name='Executive Assistant'),
            Roles(Name='Program Administrator'),
            Roles(Name='Program Manager'),
            Roles(Name='Administrative Analyst'),
            Roles(Name='Data Entry'),

            Roles(Name='CEO—Chief Executive Officer'),
            Roles(Name='COO—Chief Operating Officer'),
            Roles(Name='CFO—Chief Financial Officer'),
            Roles(Name='CIO—Chief Information Officer'),
            Roles(Name='CTO—Chief Technology Officer'),
            Roles(Name='CMO—Chief Marketing Officer'),
            Roles(Name='CHRO—Chief Human Resources Officer'),
            Roles(Name='CDO—Chief Data Officer'),
            Roles(Name='CPO—Chief Product Officer'),
            Roles(Name='CCO—Chief Customer Officer'),

            Roles(Name='Team Leader'),
            Roles(Name='Manager'),
            Roles(Name='Assistant Manager'),
            Roles(Name='Executive'),
            Roles(Name='Director'),
            Roles(Name='Coordinator'),
            Roles(Name='Administrator'),
            Roles(Name='Controller'),
            Roles(Name='Officer'),
            Roles(Name='Organizer'),
            Roles(Name='Supervisor'),
            Roles(Name='Superintendent'),
            Roles(Name='Head'),
            Roles(Name='Overseer'),
            Roles(Name='Chief'),
            Roles(Name='Foreman'),
            Roles(Name='Controller'),
            Roles(Name='Principal'),
            Roles(Name='President'),
            Roles(Name='President'),
            Roles(Name='Lead'),
            Roles(Name='Project Manager'),

            Roles(Name='Sales Associate'),
            Roles(Name='Sales Manager'),
            Roles(Name='Sales Representative'),
            Roles(Name='Retail Worker'),
            Roles(Name='Store Manager'),
            Roles(Name='Real Estate Broker'),
            Roles(Name='Cashier'),

            Roles(Name='Solar Photovoltaic Installer'),
            Roles(Name='Operations Manager'),
            ]
        dbsession.add_all(roles)

        dbsession.commit()

    return render_template("index.html")


# ------------------------------------------------------------------------ Sections ------------------------------------------------------------#
# perfect for adding the sections
@app.route("/<string:Id>/sections", methods=["GET", "POST"])
@login_required
def sections(Id):
    """ Add sections """
    form = SectionAddForm()
    u_sections = dbsession.query(Sections.Id, Sections.Name, Sections.Description, Sections.RDT).join(Users, Users.Id==Sections.UserID).where(Sections.UserID==Id).all()
    if form.validate_on_submit():
        new_section = Sections(
            Name = form.section_name.data,
            Description = form.section_description.data,
            UserID = Id
            )

        dbsession.add(new_section)
        dbsession.commit()

    return redirect("/{}/projects".format(session["user_id"]))

#---------------------------------------------------------------------------------- delete section
@app.route("/<string:Id>/section/delete/<string:sec_id>", methods=["GET", "POST"])
@login_required
def delete_section(Id, sec_id):
    """ delete sections """
    section = dbsession.query(Sections).join(Users, Users.Id==Sections.UserID).filter(Sections.Id==sec_id).first()
    dbsession.delete(section)
    dbsession.commit()
    return redirect("/{}/projects".format(Id))

#----------------------------------------------------------------------------------- edit section
@app.route("/<string:Id>/section/edit/<string:sec_id>", methods=["GET","POST"])
@login_required
def edit_section(Id, sec_id):
    """ edit sections """
    form = SectionEditForm()
    section = dbsession.query(Sections).join(Users, Users.Id==Sections.UserID).filter(Sections.Id==sec_id).first()

    if form.validate_on_submit():
        section.Name = form.e_section_name.data
        section.Description = form.e_section_description.data

        dbsession.commit()

    return redirect("/{}/projects".format(Id))



# ------------------------------------------------------------------------ Projects --------------------------------------------------------------------#
# perfect for adding the projects
@app.route("/<string:Id>/projects", methods=["GET", "POST"])
@login_required
def projects(Id):
    """ Add projects """
    form = ProjectAddForm()
    st_form = SubtaskEditForm()

    # table user projects
    t_projects = dbsession.query(Projects.Id, Projects.Name, Projects.Description, Projects.SD, Projects.DD, Sections.Id.label("Section_id"), Sections.Name.label("Section_name")).join(Sections, Sections.Id==Projects.SectionID).where(Projects.UserID==Id).all()
    # user sections including default
    all_user_sections = dbsession.query(Sections).filter(or_(Sections.UserID==Id)|(Sections.Name=='Default')).all()

    # user custom sections only
    user_sections = dbsession.query(Sections.Id, Sections.Name, Sections.Description, Sections.RDT).join(Users, Users.Id==Sections.UserID).where(Sections.UserID==Id).all()


    # user tasks
    t_tasks = dbsession.query(Tasks.Id, Tasks.Name, Tasks.Description, Tasks.SD, Tasks.DD, Tasks.ProjectID, Tasks.PriorityID, Priorities.Name.label("Priority_name"), Projects.Name.label("Project_name")).join(Priorities, Priorities.Id==Tasks.PriorityID).join(Projects, Projects.Id==Tasks.ProjectID).where(Tasks.Recorder==Id).all()

    # user subtasks
    t_subtasks = dbsession.query(Subtasks.Id, Subtasks.Name, Subtasks.Description, Subtasks.SD, Subtasks.DD, Subtasks.PriorityID, Priorities.Name.label("Priority_name"), Tasks.Id.label('Task_id'), Tasks.Name.label("Task_name"), Projects.Name.label("Project_name")).join(Priorities, Priorities.Id==Subtasks.PriorityID).join(Tasks, Tasks.Id==Subtasks.TaskID).join(Projects, Projects.Id==Tasks.ProjectID).where(Subtasks.Recorder==Id).all()

    # all priorities
    priorities = dbsession.query(Priorities).all()

    if form.validate_on_submit():

        new_project = Projects(
            Name = form.project_name.data,
            Description = form.project_description.data,
            SD = form.project_SD.data,
            DD = form.project_DD.data,
            SectionID = form.project_section.data,
            UserID = Id
            )

        dbsession.add(new_project)
        dbsession.commit()

        return redirect("/{}/projects".format(Id))

    return render_template("user/projects.html", form=form, st_form=st_form, t_projects=t_projects, all_user_sections=all_user_sections, t_tasks=t_tasks, priorities=priorities, t_subtasks=t_subtasks, user_sections=user_sections)


#------------------------------------------------------------------------------------- delete projects
@app.route("/<string:Id>/project/delete/<string:project_id>", methods=["GET", "POST"])
@login_required
def delete_project(Id, project_id):
    """ delete project """
    project = dbsession.query(Projects).filter(Projects.Id==project_id).first()
    dbsession.delete(project)
    dbsession.commit()

    return redirect("/{}/projects".format(Id))


#------------------------------------------------------------------------------------ edit projects
@app.route("/<string:Id>/project/edit/<string:project_id>", methods=["GET","POST"])
@login_required
def edit_project(Id, project_id):
    """ edit projects """
    form = ProjectEditForm()
    project = dbsession.query(Projects).filter(Projects.Id==project_id).first()

    if form.validate_on_submit():
        project.Name = form.e_project_name.data
        project.Description = form.e_project_description.data
        project.SD = form.e_project_SD.data
        project.DD = form.e_project_DD.data
        project.SectionID = form.e_project_section.data
        dbsession.commit()

    return redirect("/{}/projects".format(Id))


# ---------------------------------------------------------------------------------- Tasks --------------------------------------------------------------------------------------------------------------------#
# perfect for adding the tasks
@app.route("/<string:Id>/tasks", methods=["GET", "POST"])
@login_required
def tasks(Id):
    """ Add tasks """
    form = TaskAddForm()
    u_tasks = dbsession.query(Tasks.Id, Tasks.Name, Tasks.Description, Tasks.SD, Tasks.DD, Tasks.ProjectID, Tasks.PriorityID, Priorities.Name.label("Priority_name"), Projects.Name.label("Project_name")).join(Priorities, Priorities.Id==Tasks.PriorityID).join(Projects, Projects.Id==Tasks.ProjectID).where(Tasks.Recorder==Id).all()

    u_projects = dbsession.query(Projects).filter(Projects.UserID==Id).all()
    priorities = dbsession.query(Priorities).all()

    if form.validate_on_submit():

        new_task = Tasks(
            Name = form.task_name.data,
            Description = form.task_description.data,
            SD = form.task_SD.data,
            DD = form.task_DD.data,
            ProjectID = form.task_project.data,
            PriorityID = form.task_priority.data,
            Recorder = Id
            )

        dbsession.add(new_task)
        dbsession.commit()

    return redirect("/{}/projects".format(Id))


#---------------------------------------------------------------------------------- delete tasks
@app.route("/<string:Id>/task/delete/<string:task_id>", methods=["GET", "POST"])
@login_required
def delete_tasks(Id, task_id):
    """ delete tasks """
    task = dbsession.query(Tasks).filter(Tasks.Id==task_id).first()
    dbsession.delete(task)
    dbsession.commit()

    return redirect("/{}/projects".format(Id))


#----------------------------------------------------------------------------------- edite tasks
@app.route("/<string:Id>/task/edit/<string:task_id>", methods=["GET","POST"])
@login_required
def edit_task(Id, task_id):
    """ edit tasks """
    form = TaskEditForm()
    task = dbsession.query(Tasks).filter(Tasks.Id==task_id).first()

    if form.validate_on_submit():
        task.Name = form.e_task_name.data
        task.Description = form.e_task_description.data
        task.SD = form.e_task_SD.data
        task.DD = form.e_task_DD.data
        task.ProjectID = form.e_task_project.data
        task.PriorityID = form.e_task_priority.data
        task.Recorder = Id
        dbsession.commit()

    return redirect("/{}/projects".format(Id))



# ---------------------------------------------------------------------------------- SubTasks --------------------------------------------------------------------------------------------------------------------#
# perfect for adding the subtasks
@app.route("/<string:Id>/subtasks", methods=["GET", "POST"])
@login_required
def subtasks(Id):
    """ Add subtasks """
    form = SubtaskAddForm()
    u_subtasks = dbsession.query(Subtasks.Id, Subtasks.Name, Subtasks.Description, Subtasks.SD, Subtasks.DD, Subtasks.PriorityID, Priorities.Name.label("Priority_name"), Tasks.Id.label('Task_id'), Tasks.Name.label("Task_name"), Projects.Name.label("Project_name")).join(Priorities, Priorities.Id==Subtasks.PriorityID).join(Tasks, Tasks.Id==Subtasks.TaskID).join(Projects, Projects.Id==Tasks.ProjectID).where(Subtasks.Recorder==Id).all()

    u_tasks = dbsession.query(Tasks).filter(Tasks.Recorder==Id).all()
    priorities = dbsession.query(Priorities).all()

    if form.validate_on_submit():

        new_subtask = Subtasks(
            Name = form.subtask_name.data,
            Description = form.subtask_description.data,
            SD = form.subtask_SD.data,
            DD = form.subtask_DD.data,
            TaskID = form.subtask_task.data,
            PriorityID = form.subtask_priority.data,
            Recorder = Id
            )

        dbsession.add(new_subtask)
        dbsession.commit()

    return redirect("/{}/projects".format(Id))


#--------------------------------------------------------------------------------------- delete subtasks
@app.route("/<string:Id>/subtask/delete/<string:subtask_id>", methods=["GET", "POST"])
@login_required
def delete_subtasks(Id, subtask_id):
    """ delete subtasks """
    subtask = dbsession.query(Subtasks).filter(Subtasks.Id==subtask_id).first()
    dbsession.delete(subtask)
    dbsession.commit()

    return redirect("/{}/projects".format(Id))


#----------------------------------------------------------------------------------------- edite subtasks
@app.route("/<string:Id>/subtask/edit/<string:subtask_id>", methods=["GET","POST"])
@login_required
def edit_subtask(Id, subtask_id):
    """ edit subtasks """
    form = SubtaskEditForm()
    subtask = dbsession.query(Subtasks).filter(Subtasks.Id==subtask_id).first()

    if form.validate_on_submit():
        subtask.Name = form.e_subtask_name.data
        subtask.Description = form.e_subtask_description.data
        subtask.SDT = form.e_subtask_SD.data
        subtask.EDT = form.e_subtask_DD.data
        subtask.TaskID = form.e_subtask_task.data
        subtask.PriorityID = form.e_subtask_priority.data
        subtask.Recorder = Id
        dbsession.commit()


    return redirect("/{}/projects".format(Id))


# --------------------------------------------------------------------------- Error handler ---------------------------------------------------------------
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__=="__main__":
    app.run(debug=True)
