from sqlalchemy import create_engine #This function is used to create a new SQLAlchemy engine, which is responsible for managing the database connection and executing SQL statements.
from sqlalchemy.orm import sessionmaker #This function is used to create a session factory, which is responsible for creating new Session objects that are used to interact with the database.
from sqlalchemy.ext.declarative import declarative_base #This function is used to create a base class for the declarative models, which are used to define the structure of the database tables and their relationships.

SQLALCHEMY_DATABASE_URL = "sqlite:///todosapp.db" #Used when we are using Sqlite database
#Create a location to store the database file. The three slashes indicate a relative path, while four slashes indicate an absolute path.

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Sanxhitk999%40%23%24@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Sanxhitk999%40%23%24@127.0.0.1:3306/TodoApplicationDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#connect_args={"check_same_thread": False} is required only for SQLite. It allows the database to be accessed from different threads.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create a session factory for the database.
Base=declarative_base() # Create a base class for the declarative models.


