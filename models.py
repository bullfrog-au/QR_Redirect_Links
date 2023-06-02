from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class records(Base):
    __tablename__ = "qr"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    link = Column(String)


# schemas?