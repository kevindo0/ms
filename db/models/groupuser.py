from sqlalchemy import Column, String, Integer, SmallInteger
from sqlalchemy.schema import Index
from db import Base


class GroupUser(Base):
    __tablename__ = 'groupuser'

    # Index可以在Table参数中，声明性是通过__table_args__
    __table_args__ = (
        Index('idx_group_user_name_number', 'status', 'number'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    status = Column(SmallInteger)
    number = Column(Integer)
