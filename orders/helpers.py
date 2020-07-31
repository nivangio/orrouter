from datetime import datetime
from Item import Item
from starter import Base, BaseMixin
from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

class OrderItemsAssociation(Base, BaseMixin):
    __tablename__ = 'ORDERS_ITEMS'

    order_id = Column(Integer, ForeignKey('ORDERS.id'))

    item_id = Column(Integer, ForeignKey('ITEMS.id'))
    item = relationship(Item)

    amount = Column(Numeric)

    def to_dict(self):
        return {"item": self.item.to_options("item_name"), "quantity": int(self.amount)}



def get_arrival_boundaries(delivery_date, arrive_after, arrive_before):
    arrive_after_datetime = datetime.strptime(delivery_date + " " + arrive_after,
                                              "%Y-%m-%d %H:%M")
    arrive_before_datetime = datetime.strptime(delivery_date + " " + arrive_before,
                                               "%Y-%m-%d %H:%M")

    return (arrive_after_datetime, arrive_before_datetime)

def build_items(items_dict):
    all_items = []

    for i in items_dict:
        assoc_object = OrderItemsAssociation(amount=i["quantity"])
        assoc_object.item = Item.get_by_id(i["id"])
        all_items.append(assoc_object)

    return all_items
