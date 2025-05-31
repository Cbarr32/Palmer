from sqlalchemy import Column, String, Integer, DateTime, Float, JSON, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False)
    industry = Column(String)
    revenue_tier = Column(String)
    employee_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_tier = Column(String, default="trial")
    
    # Relationships
    users = relationship("User", back_populates="organization")
    analyses = relationship("Analysis", back_populates="organization")
    intelligence = relationship("Intelligence", back_populates="organization")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"))
    role = Column(String, default="member")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organizations.id"))
    target_url = Column(String, nullable=False)
    analysis_type = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    results = Column(JSON)
    
    # Relationships
    organization = relationship("Organization", back_populates="analyses")

class Intelligence(Base):
    __tablename__ = "intelligence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey("organizations.id"))
    intelligence_type = Column(String)
    status = Column(String, default="pending")
    insights = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="intelligence")
