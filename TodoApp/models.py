from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, index=True)
    phone_number = Column(String)

class Todos(Base):
    __tablename__ = "todos"  # Specifies the name of the table in the database.

    id = Column(Integer, primary_key=True, index=True)  # Defines the 'id' column as an integer primary key with an index.
    title = Column(String, index=True)  # Defines the 'title' column as a string with an index.
    description = Column(String, index=True)  # Defines the 'description' column as a string with an index.
    priority = Column(Integer, index=True)  # Defines the 'priority' column as an integer with an index.
    complete = Column(Boolean, default=False)  # Defines the 'completed' column as a boolean with a default value of False.
    owner_id=Column(Integer, ForeignKey("users.id"))