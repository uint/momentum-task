import os
from sqlalchemy import create_engine

from app import create_app
from core.store.sql import SqlStore
from core.store.in_mem import InMemoryStore

postgres_host = os.environ.get('POSTGRES_HOST')
postgres_db = os.environ.get('POSTGRES_DB')
postgres_user = os.environ.get('POSTGRES_USER')
postgres_pass = os.environ.get('POSTGRES_PASS')

if postgres_host is None:
    store = InMemoryStore()
else:
    engine = create_engine(f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}/{postgres_db}", echo=True)
    store = SqlStore(engine)

app = create_app(store)