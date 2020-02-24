from sqlalchemy.schema import CreateTable, CreateIndex
from db.models import GroupUser
from db import engine

# table 类型为 <class 'sqlalchemy.sql.schema.Table'>
table = GroupUser.__table__

def show_sql(stmt):
    sql = stmt.compile(engine)
    print(f'{str(sql).strip()};')

# 创建表的sql命令
show_sql(CreateTable(table))

# 创建Index的sql命令
for idx in table.indexes:
    show_sql(CreateIndex(idx))
