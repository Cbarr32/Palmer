from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.models.database import User, Organization
from backend.core.config import settings
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def get_domain_from_email(self, email: str) -> str:
        return email.split('@')[1] if '@' in email else None
    
    async def authenticate_user(self, db: Session, email: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            domain = self.get_domain_from_email(email)
            if domain:
                org = db.query(Organization).filter(Organization.domain == domain).first()
                if not org:
                    org = Organization(domain=domain, name=domain.split('.')[0].title())
                    db.add(org)
                    db.commit()
                
                user = User(email=email, organization_id=org.id)
                db.add(user)
                db.commit()
        
        user.last_login = datetime.utcnow()
        db.commit()
        return user
