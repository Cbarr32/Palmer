from sqlalchemy import create_engine
from backend.core.config import settings
from backend.models.database import Base

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
