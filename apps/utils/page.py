import math


def to_dict(obj, columns=[]):
    # 将一个对象转成字典
    if isinstance(obj, list) and len(columns) > 0:
        d = {column: getattr(obj, column, None) for column in columns}
    else:
        d = {}
        for column in obj.__table__.columns:
            d[column.name] = getattr(obj, column.name)
    return d


def pagination(obj, page, page_size=10, attrs=[]):
    # attrs: 需要获取的属性名称列表
    new_obj = []
    count = obj.count()
    if page > 1:
        objects = obj.offset((page - 1) * page_size).limit(page_size)
    else:
        objects = obj.offset((page - 1) * page_size).limit(page_size)
    for item in objects:
        new_obj.append(to_dict(item))
    res = {
        'num_results': objects.count(),
        'page': page,
        'objects': new_obj,
        'total_pages': math.ceil(count / page_size)
    }
    return res
