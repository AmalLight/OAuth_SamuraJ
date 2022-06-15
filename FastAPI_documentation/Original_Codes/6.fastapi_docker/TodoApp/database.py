from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@172.16.239.2/pgadmin"

# MYSQL Series
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234!@127.0.0.1:3306/todoapp"

engine = create_engine ( SQLALCHEMY_DATABASE_URL )

# MYSQL Series
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

SessionLocal = sessionmaker ( autocommit = False , autoflush = False , bind = engine )

Base = declarative_base ()
