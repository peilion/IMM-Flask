"""
Using this config by:

from db_config import session
session.query...    #do something

Making sure that the init_db method has been called before app run.
"""

from sqlalchemy import create_engine

table_args = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8'
}
SHARDING_NUMBER = 3
engine = create_engine('mysql://root:8315814@localhost/flask-imm', convert_unicode=True)

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
