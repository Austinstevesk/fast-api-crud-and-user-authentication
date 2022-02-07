from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:qweaz@127.0.0.1/fastapi'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
#if using sqlite, use the following
# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=false, autoflush=false, bind=engine)

#This will be extended for the models
Base = declarative_base()