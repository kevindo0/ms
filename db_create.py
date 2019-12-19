from apps.g.database import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, engine, Base
from migrate.versioning import api
import os.path
 
Base.metadata.create_all(bind=engine)
 
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))