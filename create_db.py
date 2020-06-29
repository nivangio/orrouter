from starter.db_session import Base, engine

from Client import Client
from Item import Item

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)
