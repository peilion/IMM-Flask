from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(64))
             )

manufacturer = Table('manufacturer', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String(32), unique=True),
                     Column('telephone', String(30), nullable=True)
                     )

