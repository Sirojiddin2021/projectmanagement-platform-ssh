from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import expression, func

from datetime import datetime
from pytz import timezone

Base = declarative_base()

# companies table


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


# company_management table


class CompanyManagement(Base):
    __tablename__ = "company_management"
    Id = Column('id', Integer, primary_key=True)
    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Manager = Column('is_manager', Boolean, server_default='False')


# departments table


class Departments(Base):
    __tablename__ = "departments"
    Id = Column('id', Integer, primary_key=True)
    # department data
    Name = Column('department_name', String, nullable=False)
    Status = Column('status', Boolean)
    About = Column('about_department', String)


# department_management table


class DepartmentManagement(Base):
    __tablename__ = "department_management"
    Id = Column('id', Integer, primary_key=True)
    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    DepartmentID = Column('department_id', Integer, ForeignKey('departments.id', ondelete='SET NULL'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Manager = Column('is_manager', Boolean, server_default='False')


# teams table


class Teams(Base):
    __tablename__ = "teams"
    Id = Column('id', Integer, primary_key=True)

    # team data
    Name = Column('team_name', String, nullable=False)
    Status = Column('status', Boolean)
    About = Column('about_department', String)


# team_members table


class TeamMembers(Base):
    __tablename__ = "team_members"
    Id = Column('id', Integer, primary_key=True)
    CompanyID = Column('company_id', Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    DepartmentID = Column('department_id', Integer, ForeignKey('departments.id', ondelete='SET NULL'))
    TeamID = Column('team_id', Integer, ForeignKey('teams.id', ondelete='SET NULL'), nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Leader = Column('is_leader', Boolean, server_default='False')


# users table


class Users(Base):
    __tablename__ = "users"
    Id = Column('id', Integer, primary_key=True)

    # user personal details
    Username = Column('username', String(50), unique=True, nullable=False)
    Password = Column('password', String(80), nullable=False)
    Email = Column('email', String(100), unique=True, nullable=False)
    Phone = Column('phone', String(30), server_default='')
    Firstname = Column('firstname', String(50), server_default='')
    Lastname = Column('lastname', String(50), server_default='')
    Role = Column('role', String(100), server_default='')
    About = Column('about_user', String, server_default='I am python programmer.')

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


#  user_logs table


class UserLog(Base):
    __tablename__ = "user_logs"
    Id = Column('id', Integer, primary_key=True)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Login = Column('login', DateTime)
    Logout = Column('logout', DateTime)
    Online = Column('is_online', Boolean)


# user_type table


class UserTypes(Base):
    __tablename__ = "user_type"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('type_name', String(20), unique=True, nullable=False)


# valued_users table


class ValuedUsers(Base):
    __tablename__ = "valued_users"
    Id = Column('id', Integer, primary_key=True)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    UserTypeID = Column('user_type_id', Integer, ForeignKey('user_type.id', ondelete='SET NULL'))
    SD = Column('start_date', DateTime)
    ED = Column('end_date', DateTime)
    Expired = Column('is_expired', Boolean, server_default='True')


# sections table


class Sections(Base):
    __tablename__ = "sections"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('section_name', String(100), nullable=False)
    Description = Column('section_description', String(200))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL'))
    RDT = Column('recorded_datetime', DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    Permanent = Column('is_permanent', Boolean, server_default='False')


# projects table


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


# project_messages table


class ProjectMessages(Base):
    __tablename__ = "project_messages"
    Id = Column('id', Integer, primary_key=True)
    ProjectID = Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Message = Column('message', String, nullable=False)
    DT = Column('message_date', DateTime)


# tasks table


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


# priorities table


class Priorities(Base):
    __tablename__ = "priorities"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('name', String(10))


# roles table


class Roles(Base):
    __tablename__ = "roles"
    Id = Column('id', Integer, primary_key=True)
    Name = Column('name', String(50))


# task_collaborators table


class TaskCollaborators(Base):
    __tablename__ = "task_collaborators"
    Id = Column('id', Integer, primary_key=True)
    TaskID = Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Assignee = Column('assignee', Boolean, server_default='False')


# task_messages table


class TaskMessages(Base):
    __tablename__ = "task_messages"
    Id = Column('id', Integer, primary_key=True)
    TaskID = Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Message = Column('message', String, nullable=False)
    DT = Column('message_datetime', DateTime)


# subtasks table


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


# subtask_collaborators table


class SubTaskCollaborators(Base):
    __tablename__ = "subtask_collaborators"
    Id = Column('id', Integer, primary_key=True)
    SubTaskID = Column('subtask_id', Integer, ForeignKey('subtasks.id', ondelete='CASCADE', onupdate='CASCADE'))
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
    Assignee = Column('assignee', Boolean, server_default='False')


# subtask_messages table


class SubTaskMessages(Base):
    __tablename__ = "subtask_messages"
    Id = Column('id', Integer, primary_key=True)
    SubTaskID = Column('subtask_id', Integer, ForeignKey('subtasks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    UserID = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Message = Column('message', String, nullable=False)
    DateTime = Column('message_datetime', DateTime)


engine = create_engine('sqlite:///project.db', echo=True)


def init():

    Base.metadata.create_all(bind=engine)