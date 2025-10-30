from datetime import datetime
import core
from core.store import BookAlreadyExists, BookNotFound, Store

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class Book(BaseModel):
    ident: int = Field(100000, ge=0, lt=1000000)
    title: str
    author: str

class BorrowInner(BaseModel):
    who: int = Field(100000, ge=0, lt=1000000)
    when: datetime

class Borrow(BaseModel):
    borrowed: BorrowInner | None

def create_app(store: Store):
    app = FastAPI()

    @app.post("/book")
    async def add_book(book: Book):
        try:
            store.add_book(core.store.Book(book.ident, book.title, book.author))
        except BookAlreadyExists:
            raise HTTPException(status_code=409, detail="Book already exists")

    @app.put("/book/{book_id}")
    async def update_book(book_id: int, borrow: Borrow):
        borrow_event: core.store.BorrowEvent | None = None

        if borrow.borrowed is not None:
            borrow_event = core.store.BorrowEvent(borrow.borrowed.who, borrow.borrowed.when)

        try:
            store.update_book(book_id, borrow_event)
        except BookNotFound:
            raise HTTPException(status_code=404, detail="Book not found")

    @app.delete("/book/{book_id}")
    async def delete_book(book_id: int):
        try:
            store.remove_book(book_id)
        except BookNotFound:
            raise HTTPException(status_code=404, detail="Book not found")

    @app.get("/book")
    async def list_books():
        return store.list_books()

    @app.get("/info")
    async def info():
        return {"store": type(store).__name__}

    return app