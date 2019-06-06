from db_config import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker(autocommit=False,
                       autoflush=True,
                       bind=engine)
Base = declarative_base()
