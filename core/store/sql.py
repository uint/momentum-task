from datetime import datetime
from sqlalchemy import delete, update, Engine, ForeignKey, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

from . import BookAlreadyExists, BookNotFound, Store, Book, BorrowEvent
from typing import Dict, List, Optional

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "book"

    ident: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    borrowed_to: Mapped[Optional[int]]
    borrowed_time: Mapped[Optional[datetime]]

def into_book(book_model: BookModel) -> Book:
    if book_model.borrowed_to is not None and book_model.borrowed_time is not None:
        borrowed = BorrowEvent(book_model.borrowed_to, book_model.borrowed_time)
    else:
        borrowed = None

    return Book(book_model.ident, book_model.title, book_model.author, borrowed)

class SqlStore(Store):
    def __init__(self, engine: Engine):
        Base.metadata.create_all(engine)

        self.engine = engine

    def add_book(self, book: Book):
        with Session(self.engine) as session:
            book_row: BookModel = BookModel(ident=book.ident, title=book.title, author=book.author)
            session.add(book_row)
            session.commit()

    def remove_book(self, ident: int):
        with Session(self.engine) as session:
            stmt = delete(BookModel).where(BookModel.ident == ident)
            session.execute(stmt)
            session.commit()

    def list_books(self) -> List[Book]:
        session = Session(self.engine)

        stmt = select(BookModel)
        return list(map(into_book, session.scalars(stmt)))

    def update_book(self, ident: int, borrowed: Optional[BorrowEvent]):
        if borrowed is not None:
            borrowed_to = borrowed.who
            borrowed_time = borrowed.when
        else:
            borrowed_to = None
            borrowed_time = None
        
        with Session(self.engine) as session:
            stmt = update(BookModel).where(BookModel.ident == ident).values(borrowed_to=borrowed_to, borrowed_time=borrowed_time)
            session.execute(stmt)
            session.commit()
