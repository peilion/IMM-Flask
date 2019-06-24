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
engine = create_engine('mysql://git:Fpl8315814.@123.56.7.137/imm-prod', convert_unicode=True)

admin_engine = create_engine('mysql://git:Fpl8315814.@123.56.7.137/information_schema', convert_unicode=True)
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
SHARDING_NUMBER = 3
