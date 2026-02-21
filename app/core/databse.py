from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import app_settings

# create engine
engine = create_engine(url=app_settings.db_url)

# bind with sqlurl 
LocalSession = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Bases for all tables
Base = declarative_base()


