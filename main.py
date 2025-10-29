from sqlalchemy import create_engine

from app import create_app
from core.store.sql import SqlStore

engine = create_engine("sqlite://", echo=True)
app = create_app(SqlStore(engine))