import os
from contextlib import contextmanager
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dynaconf import settings

from apps.utils import logger
from apps.utils import exceptions

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    settings.DB_USER, settings.DB_PASSWORD,
    settings.DB_HOST, settings.DB_PORT,
    settings.DATABASE)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='utf-8')

Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def db_session():
    sess = Session()
    try:
        yield sess
        sess.commit()
    except Exception as ex:
        sess.rollback()
        raise exceptions.MysqlError(info=ex)
    finally:
        sess.close()


# scoped_session 线程安全
@contextmanager
def session():
    sess = scoped_session(Session)()
    try:
        yield sess
        sess.commit()
    except Exception as ex:
        sess.rollback()
        logger.exception(ex)
    finally:
        sess.close()
