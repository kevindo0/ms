from contextlib import contextmanager
from sqlalchemy import create_engine
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dynaconf import settings

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    settings.DB_USER, settings.DB_PASSWORD, 
    settings.DB_HOST, settings.DB_PORT, 
    settings.DATABASE)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='utf-8')

db = sessionmaker(bind=engine)()
Base = declarative_base()

@contextmanager
def db_session():
    try:
        yield db
        db.commit()
    except Exception as ex:
        db.rollback()
        raise exceptions.DatabaseError(info=ex)
    finally:
        db.close()
