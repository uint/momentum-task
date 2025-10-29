from app import create_app
from core.store.in_mem import InMemoryStore

app = create_app(InMemoryStore())