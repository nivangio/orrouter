from sqlalchemy import Column, Integer
from .db_session import db_session
from helpers import sql_alchemy_object_to_dict

class Static(object):

    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.upper()

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls,id):
        ret = db_session.query(cls).filter_by(id=id).first()
        return ret

    @classmethod
    def get(cls, multiple = True, **kwargs):

        if multiple:
            ret = db_session.query(cls).filter_by(**kwargs).all()
        else:
            ret = db_session.query(cls).filter_by(**kwargs).first()

        return ret

    @classmethod
    def get_all(cls):
        ret = db_session.query(cls).all()
        return ret

    @classmethod
    def get_multiple_by_id(cls, id_list):
        ret = db_session.query(cls).filter(cls.id.in_(id_list)).all()
        return ret

    def to_dict(self, variables = "all"):
        return sql_alchemy_object_to_dict(self, variables)