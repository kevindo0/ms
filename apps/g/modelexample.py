from sqlalchemy import Column, String, Integer
from apps.g.database import Base

class GroupUser(Base):
    __tablename__ = 'groupuser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
