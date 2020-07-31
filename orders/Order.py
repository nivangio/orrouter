from starter import Base, BaseMixin, db_session
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .OrderStatus import OrderStatus
from datetime import datetime
from .helpers import get_arrival_boundaries, build_items, OrderItemsAssociation

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
        self.items = build_items(kwargs.pop("items"))
        self.arrive_after, self.arrive_before = get_arrival_boundaries(kwargs["delivery_date"], kwargs["arrive_after"], kwargs["arrive_before"])
        self.client_id = kwargs["client_id"]

    def update(self, **kwargs):
        self.items = build_items(kwargs.pop("items"))
        self.arrive_after, self.arrive_before = get_arrival_boundaries(kwargs["delivery_date"], kwargs["arrive_after"], kwargs["arrive_before"])
        self.client_id = kwargs["client_id"]

        db_session.commit()

    ##This service is used to display orders in a table
    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.to_options("company_name"),
            "company_name": self.client.company_name,
            "address": self.client.display_address(),
            "delivery_date": self.arrive_after.strftime("%Y-%m-%d"),
            "arrive_after": self.arrive_after.strftime("%H:%M"),
            "arrive_before": self.arrive_before.strftime("%H:%M"),
            "total_volume": self.total_volume(),
            "order": list(map(lambda x: x.to_dict(), self.items)),
            "status": self.status.order_status_name
        }

    def total_volume(self):
        ret = sum(map(lambda x: int(x.item.volume) * int(x.amount), self.items))
        return ret