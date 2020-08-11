from .db_session import db_session
from .Searchable import Searchable
from sqlalchemy import Column, Integer
from helpers import sql_alchemy_object_to_dict, to_proper

class BaseMixin(Searchable):

    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.upper()

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db_session.add(obj)
        db_session.commit()
        return obj

    @classmethod
    def get_or_create(cls, **kwargs):
        ret = db_session.query(cls).filter_by(**kwargs).first()
        if ret is None:
            ret = cls(**kwargs)
        return ret

    @classmethod
    def get_metadata_dict(cls):
        ret = [{'value': i.name, 'text': to_proper(i.name)} for i in cls.__table__.columns if i.name not in ["id"]]
        return ret


    def to_dict(self):
        return sql_alchemy_object_to_dict(self)

    def to_options(self, label_col):
        return {'id': self.id, 'text': getattr(self,label_col)}

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


