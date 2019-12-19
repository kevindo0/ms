from sqlalchemy import Column, Integer, DateTime, func

class TableBase():
    """
    所有表公共字段和公共方法
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def to_dict(self, exclude_columns=None):
        if exclude_columns is None:
            exclude_columns = []
        d = {}
        for column in self.__table__.columns:
            if column.name in exclude_columns:
                continue
            d[column.name] = getattr(self, column.name)
        return d
