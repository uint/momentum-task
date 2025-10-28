from . import Store, Book, BorrowEvent
from typing import Dict, List, Optional

class InMemoryStore(Store):
    def __init__(self):
        self.books: Dict[int, Book] = dict()

    def add_book(self, book: Book):
        if book.ident in self.books:
            raise "aa"
        else:
            self.books[book.ident] = book

    def remove_book(self, ident: int):
        del self.books[ident]

    def list_books(self) -> List[Book]:
        return list(self.books.values())

    def update_book(self, ident: int, borrowed: Optional[BorrowEvent]):
        self.books[ident].borrowed = borrowed
