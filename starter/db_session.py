from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from json import load as jsonload

# #DB Read
# with open("config.json", "r") as f:
#        connection_data = jsonload(f)["connection"]

##Engine Local
engine = create_engine('postgresql://hernan@localhost:5432/pgrouting')

db_session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))



Base = declarative_base()