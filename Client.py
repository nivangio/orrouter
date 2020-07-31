from starter import BaseMixin, Base
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from orders import Order

class Client(Base, BaseMixin):
    __tablename__ = "CLIENTS"

    company_name = Column(String)
    contact_name = Column(String)
    address = Column(JSON)

    orders = relationship(Order, backref="client")

    def display_address(self):

        if "name" in self.address["properties"].keys():
            address_display = self.address["properties"]["name"]
        else:
            address_display = self.address["properties"]["street"] + " " + self.address["properties"]["housenumber"]

        return ", ".join([address_display, self.address["properties"].get("city",'')])
