from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import expression, func

from datetime import datetime
from pytz import timezone



Base = declarative_base()

class Companies(Base):
    __tablename__ = "companies"
    Id = Column('id', Integer, primary_key=True)

    # company data
    Name = Column('company_name', String, nullable=False)
    Address = Column('address', String)
    City = Column('city', String(100))
    Zip = Column('zip', String(10))
    Phone = Column('phone', String(30))
    State = Column('state', String(100))
    Founded = Column('founded_year', Date)
    Status = Column('status', Boolean)
    About = Column('about_company', String)
    Employees = Column('employees', Integer)


    """
    CREATE TABLE companies (
id INTEGER NOT NULL,
company_name VARCHAR NOT NULL,
address VARCHAR,
city VARCHAR(100),
zip VARCHAR(10),
phone VARCHAR(30),
state VARCHAR(100),
founded_year DATE,
status BOOLEAN,
about_company VARCHAR,
employees INTEGER,
PRIMARY KEY (id)
)

    """


class CompanyManagement(Base):
    __tablename__ = "company_management"
    Id = Column('id', Integer, primary_key=True)
    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Manager = Column('is_manager', Boolean, server_default='False')

    """

    CREATE TABLE company_management (
id INTEGER NOT NULL,
company_id INTEGER,
user_id INTEGER,
is_manager BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE SET NULL,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)

    """

class Departments(Base):
    __tablename__ = "departments"
    Id = Column('id', Integer, primary_key=True)
    # department data
    Name = Column('department_name', String, nullable=False)
    Status = Column('status', Boolean)
    About = Column('about_department', String)

    """
    CREATE TABLE departments (
id INTEGER NOT NULL,
department_name VARCHAR NOT NULL,
status BOOLEAN,
about_department VARCHAR,
PRIMARY KEY (id)
)

    """
class DepartmentManagement(Base):
    __tablename__ = "department_management"
    Id = Column('id', Integer, primary_key=True)
    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    DepartmentID = Column('department_id', Integer, ForeignKey('departments.id', ondelete='SET NULL'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Manager = Column('is_manager', Boolean, server_default='False')

    """
    CREATE TABLE department_management (
id INTEGER NOT NULL,
company_id INTEGER,
department_id INTEGER,
user_id INTEGER,
is_manager BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE SET NULL,
FOREIGN KEY(department_id) REFERENCES departments (id) ON DELETE SET NULL,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """


class Teams(Base):
    __tablename__ = "teams"
    Id = Column('id', Integer, primary_key=True)

    # team data
    Name = Column('team_name', String, nullable=False)
    Status = Column('status', Boolean)
    About = Column('about_department', String)

    """
    CREATE TABLE teams (
id INTEGER NOT NULL,
team_name VARCHAR NOT NULL,
status BOOLEAN,
about_department VARCHAR,
PRIMARY KEY (id)
)
    """

class TeamMembers(Base):
    __tablename__ = "team_members"

    Id = Column('id', Integer, primary_key=True)

    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    DepartmentID = Column('department_id', Integer, ForeignKey('departments.id', ondelete='SET NULL'))
    TeamID = Column('team_id', Integer, ForeignKey('teams.id', ondelete='SET NULL') , nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Leader = Column('is_leader', Boolean, server_default='False')

    """
    CREATE TABLE team_members (
id INTEGER NOT NULL,
company_id INTEGER,
department_id INTEGER,
team_id INTEGER NOT NULL,
user_id INTEGER,
is_leader BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE SET NULL,
FOREIGN KEY(department_id) REFERENCES departments (id) ON DELETE SET NULL,
FOREIGN KEY(team_id) REFERENCES teams (id) ON DELETE SET NULL,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """

class Users(Base):
    __tablename__ = "users"
    Id = Column('id', Integer, primary_key=True)

    # user personal details
    Username = Column('username', String(50), unique=True, nullable=False)
    Password = Column('password', String(80), nullable=False)
    Email = Column('email', String(100), unique=True, nullable=False)
    Phone =Column('phone', String(30), server_default='')
    Firstname = Column('firstname', String(50), server_default='')
    Lastname = Column('lastname', String(50), server_default='')
    Role = Column('role', String(100), server_default='')
    About = Column('about_user', String, server_default='I usually work from 9am-5pm PST. Feel free to assign me a task with a due date anytime.')

    # user rate per hour in USD
    Rate = Column('rate', Float, server_default='0.0')

    # is user project manager? if yes he needs to purchase package
    Project_manager = Column('is_project_manager', Boolean, server_default='False')
    # registration date and time
    RegDT = Column('registration_datetime', DateTime, server_default=str(datetime.now()))
    # if user confirmed through email
    IsConfirmed = Column('is_confirmed', Boolean, server_default='False')
    # user current status (online/offline)
    Status = Column('status', Boolean, server_default='False')

    # these below two options not available through website registration
    # is user admin? (related to the website management) cannot manage or change any other administrators
    Admin = Column('is_admin', Boolean, server_default='False')
    # is user superadmin (only who manages website) superadmin has right to promote any user to website administrator or vise versa
    SuperAdmin = Column('is_super_admin', Boolean, server_default='False')



    """
    CREATE TABLE users (
id INTEGER NOT NULL,
username VARCHAR(50) NOT NULL,
password VARCHAR(50) NOT NULL,
email VARCHAR(100) NOT NULL,
phone VARCHAR(30),
firstname VARCHAR(50),
lastname VARCHAR(50),
role VARCHAR(100),
about_user VARCHAR DEFAULT 'I usually work from 9am-5pm PST. Feel free to assign me a task with a due date anytime.',
rate FLOAT,
is_project_manager BOOLEAN DEFAULT 'False',
registration_datetime DATETIME DEFAULT '2021-08-26 09:26:18.875550',
is_confirmed BOOLEAN DEFAULT 'False',
status BOOLEAN DEFAULT 'False',
is_admin BOOLEAN DEFAULT 'False',
is_super_admin BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
UNIQUE (username),
UNIQUE (email)
)
    """


class UserLog(Base):
    __tablename__ = "user_logs"
    Id = Column('id', Integer, primary_key=True)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Login = Column('login', DateTime)
    Logout = Column('logout', DateTime)
    Online = Column('is_online', Boolean)

    """
    CREATE TABLE user_logs (
id INTEGER NOT NULL,
user_id INTEGER,
login DATETIME,
logout DATETIME,
is_online BOOLEAN,
PRIMARY KEY (id),
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)

    """

class UserTypes(Base):
    __tablename__ = "user_type"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('type_name', String(20), unique=True, nullable=False)

    """
    CREATE TABLE user_type (
id INTEGER NOT NULL,
type_name VARCHAR(20) NOT NULL,
PRIMARY KEY (id),
UNIQUE (type_name)
)

    """
class ValuedUsers(Base):
    __tablename__ = "valued_users"
    Id = Column('id', Integer, primary_key=True)

    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE') , nullable=False)
    UserTypeID = Column('user_type_id', Integer, ForeignKey('user_type.id', ondelete='SET NULL'))

    SD = Column('start_date', DateTime)
    ED = Column('end_date', DateTime)
    Expired = Column('is_expired', Boolean, server_default='True')


    """
    CREATE TABLE valued_users (
id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
user_type_id INTEGER,
start_date DATETIME,
end_date DATETIME,
is_expired BOOLEAN DEFAULT 'True',
PRIMARY KEY (id),
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_type_id) REFERENCES user_type (id) ON DELETE SET NULL
)

    """
class Sections(Base):
    __tablename__ = "sections"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('section_name', String(100), nullable=False)
    Description = Column('section_description', String(200))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL'))
    RDT = Column('recorded_datetime', DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    Permanent = Column('is_permanent', Boolean, server_default='False')

    """
    CREATE TABLE sections (
id INTEGER NOT NULL,
section_name VARCHAR(100) NOT NULL,
PRIMARY KEY (id)
)


    """
class Projects(Base):
    __tablename__ = "projects"
    Id = Column('id', Integer, primary_key=True)

    Name = Column('project_name', String(100), nullable=False)
    Description = Column('project_description', String(200))
    SD = Column('planned_start_date', Date)
    DD = Column('planned_end_date', Date)
    ActualSD = Column('actual_start_date', Date)
    ActualED = Column('actual_end_date', Date)
    SectionID = Column('section_id', Integer, ForeignKey('sections.id', ondelete='SET NULL'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL'))
    RDT = Column('recorded_datetime', DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    """
    CREATE TABLE projects (
id INTEGER NOT NULL,
project_name VARCHAR(100) NOT NULL,
project_description VARCHAR,
planned_start_date DATE,
planned_end_date DATE,
actual_start_date DATE,
actual_end_date DATE,
PRIMARY KEY (id)
)

    """


class ProjectMessages(Base):
    __tablename__ = "project_messages"
    Id = Column('id', Integer, primary_key=True)
    ProjectID = Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Message = Column('message', String, nullable=False)
    DT = Column('message_date', DateTime)

    """
    CREATE TABLE project_messages (
id INTEGER NOT NULL,
project_id INTEGER,
user_id INTEGER,
message VARCHAR NOT NULL,
message_date DATETIME,
PRIMARY KEY (id),
FOREIGN KEY(project_id) REFERENCES projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """


class Tasks(Base):
    __tablename__ = "tasks"
    Id = Column('id', Integer, primary_key=True)

    Name = Column('task_name', String(100), nullable=False)
    Description = Column('description', String(200))
    SD = Column('start_date', Date)
    DD = Column('due_date', Date)
    ActualSDT = Column('actual_start_datetime', DateTime)
    ActualEDT = Column('actual_end_datetime', DateTime)
    Completed = Column('is_completed', Boolean, server_default='False')
    PriorityID = Column('priority_id', Integer, ForeignKey('priorities.id', ondelete='SET NULL'))
    ProjectID = Column('project_id', Integer, ForeignKey('projects.id', ondelete='SET NULL'))

    # recorder id and recorded time
    Recorder = Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL'))
    RecordDT = Column('recorded_datetime', DateTime)

    """


    """

class Priorities(Base):
    __tablename__ = "priorities"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('name', String(10))


    """

    """

class Roles(Base):
    __tablename__ = "roles"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('name', String(50))


class TaskCollaborators(Base):
    __tablename__ = "task_collaborators"
    Id = Column('id', Integer, primary_key=True)


    TaskID = Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))

    Assignee = Column('assignee', Boolean, server_default='False')



    """
    CREATE TABLE task_collaborators (
id INTEGER NOT NULL,
task_id INTEGER,
user_id INTEGER,
assignee BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
FOREIGN KEY(task_id) REFERENCES tasks (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """

class TaskMessages(Base):
    __tablename__ = "task_messages"
    Id = Column('id', Integer, primary_key=True)
    TaskID = Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Message = Column('message', String, nullable=False)
    DT = Column('message_datetime', DateTime)

    """
    CREATE TABLE task_messages (
id INTEGER NOT NULL,
task_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
message VARCHAR NOT NULL,
message_datetime DATETIME,
PRIMARY KEY (id),
FOREIGN KEY(task_id) REFERENCES tasks (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """


class Subtasks(Base):
    __tablename__ = "subtasks"
    Id = Column('id', Integer, primary_key=True)

    Name = Column('subtask_name', String(100), nullable=False)
    Description = Column('description', String(200))
    SD = Column('start_date', Date)
    DD = Column('due_date', Date)
    Completed = Column('is_completed', Boolean)
    TaskID = Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'))
    PriorityID = Column('priority_id', Integer, ForeignKey('priorities.id', ondelete='SET NULL'))

    # recorder id and recorded time
    Recorder = Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL'))
    RecordDT = Column('recorded_datetime', DateTime)

    """
    CREATE TABLE subtasks (
id INTEGER NOT NULL,
subtask_name VARCHAR(100) NOT NULL,
description VARCHAR,
priority INTEGER NOT NULL,
start_datetime DATETIME,
end_datetime DATETIME,
actual_start_datetime DATETIME,
actual_end_datetime DATETIME,
is_completed BOOLEAN,
task_id INTEGER,
PRIMARY KEY (id),
FOREIGN KEY(task_id) REFERENCES tasks (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """
class SubTaskCollaborators(Base):
    __tablename__ = "subtask_collaborators"
    Id = Column('id', Integer, primary_key=True)
    SubTaskID = Column('subtask_id', Integer, ForeignKey('subtasks.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Assignee = Column('assignee', Boolean, server_default='False')

    """
    CREATE TABLE subtask_collaborators (
id INTEGER NOT NULL,
subtask_id INTEGER,
user_id INTEGER,
assignee BOOLEAN DEFAULT 'False',
PRIMARY KEY (id),
FOREIGN KEY(subtask_id) REFERENCES subtasks (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)

    """


class SubTaskMessages(Base):
    __tablename__ = "subtask_messages"
    Id = Column('id', Integer, primary_key=True)
    SubTaskID = Column('subtask_id', Integer, ForeignKey('subtasks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Message = Column('message', String, nullable=False)
    DateTime = Column('message_datetime', DateTime)

    """
    CREATE TABLE subtask_messages (
id INTEGER NOT NULL,
subtask_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
message VARCHAR NOT NULL,
message_datetime DATETIME,
PRIMARY KEY (id),
FOREIGN KEY(subtask_id) REFERENCES subtasks (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)
    """
engine = create_engine('sqlite:///project.db', echo=True)
def init():

    Base.metadata.create_all(bind=engine)


