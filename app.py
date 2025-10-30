from datetime import datetime
import core
from core.store import Store

from fastapi import FastAPI
from pydantic import BaseModel

class Book(BaseModel):
    ident: int
    title: str
    author: str

class BorrowInner(BaseModel):
    who: int
    when: datetime

class Borrow(BaseModel):
    borrowed: BorrowInner | None

def create_app(store: Store):
    app = FastAPI()

    @app.post("/book")
    async def add_book(book: Book):
        store.add_book(core.store.Book(book.ident, book.title, book.author))

    @app.put("/book/{book_id}")
    async def update_book(book_id: int, borrow: Borrow):
        borrow_event: core.store.BorrowEvent | None = None

        if borrow.borrowed is not None:
            borrow_event = core.store.BorrowEvent(borrow.borrowed.who, borrow.borrowed.when)

        store.update_book(book_id, borrow_event)

    @app.delete("/book/{book_id}")
    async def delete_book(book_id: int):
        return store.remove_book(book_id)

    @app.get("/book")
    async def list_books():
        return store.list_books()

    @app.get("/info")
    async def info():
        return {"store": type(store).__name__}

    return app