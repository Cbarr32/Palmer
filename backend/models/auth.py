from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    organization_id: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrganizationResponse(BaseModel):
    id: str
    name: str
    domain: str
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True
