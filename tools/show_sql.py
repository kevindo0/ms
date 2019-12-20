from sqlalchemy.schema import CreateTable, CreateIndex

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Index

uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/ms?charset=utf8'

engine = create_engine(uri, encoding='utf-8')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_address', 'address'),
    )
    username = Column(String(50), primary_key=True)
    address = Column(String(50))

# table 类型为 <class 'sqlalchemy.sql.schema.Table'>
table = User.__table__

def show_sql(stmt):
    sql = stmt.compile(engine)
    print(f'{str(sql).strip()};')

# 创建表的sql命令
show_sql(CreateTable(table))

# 创建Index的sql命令
for idx in table.indexes:
    show_sql(CreateIndex(idx))
