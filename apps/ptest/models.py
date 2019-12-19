from apps.g.models import TableBase
from apps.g.database import Base
from sqlalchemy import Column, Integer, String, SmallInteger

class User(TableBase, Base):
    __tablename__ = 'user'
    name = Column(String(64))
    address = Column(String(255))
    '''
    0: 禁用
    1: 启用
    2: 删除
    '''
    status = Column(SmallInteger, default=1)
    