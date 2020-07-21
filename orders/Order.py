from starter import Base, BaseMixin, db_session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from Item import Item
from .OrderStatus import OrderStatus
from datetime import datetime

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

    order_date = Column(DateTime, default=datetime.utcnow())
    last_modified = Column(DateTime, default=datetime.utcnow())

    ##INIT: Items must be a list of dicts {"item_id":, "amount":}
    def __init__(self, **kwargs):
        self.status_id = 1

        all_items = []
        for i in kwargs.pop("items"):
            assoc_object = OrderItemsAssociation(amount=i["quantity"])
            assoc_object.item = Item.get_by_id(i["id"])
            all_items.append(assoc_object)

        self.items = all_items

        arrive_after_datetime = datetime.strptime(kwargs["delivery_date"] + " " + kwargs["arrive_after"],
                                                  "%Y-%m-%d %H:%M")
        arrive_before_datetime = datetime.strptime(kwargs["delivery_date"] + " " + kwargs["arrive_before"],
                                                  "%Y-%m-%d %H:%M")

        self.arrive_after = arrive_after_datetime
        self.arrive_before = arrive_before_datetime

        self.client_id = kwargs["client_id"]

    ##This service is used to display orders in a table
    def to_dict(self):
        return {
            "client": self.client.company_name,
            "address": self.client.address,
            "arrive_after": self.arrive_after,
            "arrive_before": self.arrive_before,
            "total_volume": self.total_volume(),
            "status": self.status.order_status_name
        }

    def total_volume(self):
        ret = sum(map(lambda x: int(x.item.volume) * int(x.amount), self.items))
        return ret