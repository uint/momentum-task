from . import BookAlreadyExists, BookNotFound, Store, Book, BorrowEvent
from typing import Dict, List, Optional
from threading import Lock

class InMemoryStore(Store):
    def __init__(self):
        self.books: Dict[int, Book] = dict()
        self.mutex = Lock()

    def add_book(self, book: Book):
        with self.mutex:
            if book.ident in self.books:
                raise BookAlreadyExists
            else:
                self.books[book.ident] = book

    def remove_book(self, ident: int):
        with self.mutex:
            try:
                del self.books[ident]
            except KeyError:
                raise BookNotFound

    def list_books(self) -> List[Book]:
        with self.mutex:
            return list(self.books.values())

    def update_book(self, ident: int, borrowed: Optional[BorrowEvent]):
        with self.mutex:
            try:
                self.books[ident].borrowed = borrowed
            except KeyError:
                raise BookNotFound
