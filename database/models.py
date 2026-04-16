from sqlalchemy import Column, Integer, String
from database.db import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(String)
    sentiment = Column(String)
    summary = Column(String)
    category = Column(String)
    priority = Column(String)
    response = Column(String)
