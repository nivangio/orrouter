from starter.db_session import Base, engine

from Client import Client

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)
