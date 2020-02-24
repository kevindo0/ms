from sqlalchemy.inspection import inspect
from db import session
from db.models import GroupUser


def get_by_pks(model, **kwargs):
    return (
        tuple(
            kwargs[key.name]
            for key in inspect(model).primary_key
        )
    )


with session() as sess:
    g = sess.query(GroupUser).get(get_by_pks(GroupUser, id=8))
    # SELECT groupuser.id AS groupuser_id, groupuser.name AS groupuser_name,
    # groupuser.status AS groupuser_status,
    # groupuser.number AS groupuser_number
    # FROM groupuser
    # WHERE groupuser.id = 8
    print('g:', g)
