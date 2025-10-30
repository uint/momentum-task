import copy
from datetime import datetime
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine

from core.store import Book, BorrowEvent
from core.store.sql import SqlStore

book1 = Book(1, "Learned Optimism", "Martin Seligman")
book2 = Book(2, "The Social Animal", "Elliot Aronson")
time = datetime.now()
borrow_event = BorrowEvent(8, time)
borrowed_book1 = copy.copy(book1)
borrowed_book1.borrowed = borrow_event

@pytest.fixture()
def store():
    engine = create_engine("sqlite://", echo=True)
    store = SqlStore(engine)
    yield store

def test_empty_by_default(store):
    assert store.list_books() == []

def test_add_book(store):
    store.add_book(book1)

    assert store.list_books() == [book1]

def test_remove_book(store):
    store.add_book(book1)
    store.add_book(book2)
    store.remove_book(book1.ident)

    assert store.list_books() == [book2]

def test_update_book(store):
    store.add_book(book1)
    store.update_book(book1.ident, borrow_event)

    assert store.list_books() == [borrowed_book1]

    store.update_book(book1.ident, None)
    assert store.list_books() == [book1]