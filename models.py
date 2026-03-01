from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base


# --------------------
# User Model
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


# --------------------
# Project Model
# --------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String, nullable=False)
    techstack = Column(String, nullable=False)  # store as comma separated string
    live_link = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True)