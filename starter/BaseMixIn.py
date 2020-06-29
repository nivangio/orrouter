from .db_session import db_session
from sqlalchemy import Column, Integer
from helpers import sql_alchemy_object_to_dict

class BaseMixin(object):

    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.upper()

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db_session.add(obj)
        db_session.commit()
        return obj.id

    @classmethod
    def get_all(cls):
        ret = db_session.query(cls).all()
        return ret

    @classmethod
    def get_by_id(cls,id):
        ret = db_session.query(cls).filter_by(id=id).first()
        return ret

    @classmethod
    def get_multiple_by_id(cls, id_list):
        ret = db_session.query(cls).filter(cls.id.in_(id_list)).all()
        return ret

    @classmethod
    def get(cls, multiple = True, **kwargs):

        if multiple:
            ret = db_session.query(cls).filter_by(**kwargs).all()
        else:
            ret = db_session.query(cls).filter_by(**kwargs).first()

        return ret

    @classmethod
    def get_or_create(cls, **kwargs):
        ret = db_session.query(cls).filter_by(**kwargs).first()
        if ret is None:
            ret = cls(**kwargs)
        return ret


    def to_dict(self):
        return sql_alchemy_object_to_dict(self)

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def send_to_db(self):
        db_session.add(self)
        db_session.commit()

    @staticmethod
    def rollback():
        db_session.rollback()

    @staticmethod
    def commit():
        db_session.commit()

    def update(self, **kw):
        for k,v in dict(**kw).items():
            setattr(self, k,v)
        db_session.commit()


