from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

#This file sets up the database connection using SQLAlchemy.
#It creates an engine using the DATABASE_URL from the config,
#And defines a SessionLocal class for creating database sessions.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}

)
#The connect_args={"check_same_thread": False} is specific to SQLite databases and allows the same connection to be used across multiple threads
#necessary for web applications that handle concurrent requests.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#The Base class is a declarative base that our ORM models will inherit from. 
#It provides the foundation for defining our database schema using SQLAlchemy's ORM features.
Base = declarative_base()

#The get_db function is a dependency that can be used in FastAPI routes to get a database session.
#It creates a new session, yields it for use in the route, and ensures that the session is closed after the request is processed, preventing potential database connection leaks.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
