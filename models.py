from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Session(Base):
    __tablename__ = 'sessions'

    session_name = Column(String(), primary_key=True, unique=True)
    api_id = Column(Integer(), primary_key=True)
    api_hash = Column(String(), primary_key=True)
    bot_token = Column(String(), primary_key=True)
    default_user = Column(String())
