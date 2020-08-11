from starter import BaseMixin, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship

class Item(Base, BaseMixin):
    __tablename__ = "ITEMS"

    user_id = Column(Integer, ForeignKey('USERS.id'))
    item_name = Column(String)
    description = Column(String)
    volume = Column(Float)

    #classes = relationship(FaresAssociation)
    #last_modified = Column(DateTime, default=datetime.utcnow())

    # def __init__(self, fares_tuples_list, cabin):
    #
    #     self.cabin = Cabin.get(cabin_name = cabin, multiple=False)
    #     self.classes = build_fares_vector(fares_tuples_list)
