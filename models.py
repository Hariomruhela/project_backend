from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# --------------------
# User Model
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)


# --------------------
# Project Model
# --------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=False)
    techstack = Column(String(255), nullable=False)  # comma separated
    live_link = Column(String(255), nullable=True)
    is_visible = Column(Boolean, default=True)
     # ✅ ADD THESE
    category = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)