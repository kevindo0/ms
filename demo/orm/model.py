from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/ms?charset=utf8'

engine = create_engine(uri, encoding='utf-8')

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=64), comment='姓名')
    mobile = Column(String(length=13), comment='手机号')
    id_card_number = Column(String(length=64), comment='身份证')

    def __str__(self):
        return '%s(name=%r,mobile=%r,id_card_number=%r)' % (
            self.__class__.__name__,
            self.name,
            self.mobile,
            self.id_card_number
        )
