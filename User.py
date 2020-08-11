from starter import Base, BaseMixin, db_session, HasAddress
from bcrypt import checkpw, hashpw, gensalt
import jwt
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, JSON

class User(Base, BaseMixin, HasAddress):
    __tablename__ = "USERS"

    username = Column(String)
    hash = Column(String)
    last_modified = Column(DateTime)
    address = Column(JSON)

    def __init__(self, username, password):
        self.username = username
        self.hash = hashpw(password.encode(), gensalt()).decode()
        self.last_modified = datetime.utcnow()

    def check_credentials(self, password, secret_key):
        try:
            if not checkpw(password.encode(), self.hash.encode()):
                raise ValueError("Incorrect Username or password")

            token = jwt.encode({"user_id": self.id, "iat": datetime.utcnow(),
                                "exp": datetime.utcnow() + timedelta(days=30)}, secret_key)
            return {"token": token.decode("utf-8")}

        except:
            raise ValueError("Incorrect Username or password")

    def change_password(self, new_password):
        self.hash = hashpw(new_password.encode(), gensalt()).decode()
        self.last_modified = datetime.utcnow()
        db_session.commit()

    def to_dict(self):
        ret = {
            "username": self.username,
            "address":self.address
        }

        return ret