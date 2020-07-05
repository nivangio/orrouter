from starter import Base, BaseMixin, db_session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from Item import Item
from .OrderStatus import OrderStatus


class OrderItemsAssociation(Base, BaseMixin):
    __tablename__ = 'ORDERS_ITEMS'

    order_id = Column(Integer, ForeignKey('ORDERS.id'))

    item_id = Column(Integer, ForeignKey('ITEMS.id'))
    item = relationship(Item)

    amount = Column(Numeric)


class Order(Base, BaseMixin):
    __tablename__ = 'ORDERS'

    client_id = Column(Integer, ForeignKey('CLIENTS.id'))

    items = relationship(OrderItemsAssociation)

    status_id = Column(Integer, ForeignKey('ORDER_STATUSES.id'))
    status = relationship(OrderStatus)

    arrive_before = Column(DateTime, nullable=True)
    arrive_after = Column(DateTime, nullable=True)

    last_modified = Column(DateTime, default=datetime.utcnow())

    ##INIT: Items must be a list of dicts {"item_id":, "amount":}
    def __init__(self, items_dict):
        self.status_id = 1

        all_items = []
        for i in items_dict:
            assoc_object = OrderItemsAssociation(amount=i["amount"])
            assoc_object.item = Item.get_by_id(i["item_id"])
            all_items.append(assoc_object)

        self.items = all_items

    ##This service is used to display orders in a table
    def to_dict(self):
        return {
            "client": self.client.company_name,
            "address": self.client.address,
            "delivery_from": self.arrive_after,
            "delivery_to": self.arrive_before,
            "status": self.status.order_status_name
        }