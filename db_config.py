"""
Using this config by:

from db_config import session
session.query...    #do something

Making sure that the init_db method has been called before app run.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

table_args = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8'
}

SHARDING_NUMBER = 3

engine = create_engine('mysql://root:8315814@localhost/flask', convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()
Base.query = Session.query_property()

from models.models import *
from models.sharding_models import *
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
