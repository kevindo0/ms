### 1. alembic
```bash
pip install alembic
# alembic初始化 init的名称自定义
alembic init alembic
# 在alembic.ini中设置数据库连接。
sqlalchemy.url = driver://user:pass@localhost/dbname
# 需要在env.py中设置，将target_metadata赋值成数据库的元数据(metadata)
# 为了使用模型类更新数据库，需要在在alembic/env.py中设置
import os
import sys
sys.path.append(os.getcwd())
from apps.g.database import Base
import apps.ptest.models
target_metadata = Base.metadata
# 创建数据迁移版本
alembic revision –autogenerate -m "create_user_table"
# 更新数据库
alembic upgrade _version
# 更新到最新版
alembic upgrade head
# 降级数据库
alembic downgrade _version
# 离线更新（生成sql）
alembic upgrade 版本号 –sql > migration.sql
```