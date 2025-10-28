from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

class BorrowEvent:
    def __init__(self, who: int, when: datetime):
        self.who = who
        self.when = when

class Book:
    def __init__(self, ident: int, title: str, author: str, borrowed: Optional[BorrowEvent] = None):
        self.ident = ident
        self.title = title
        self.author = author
        self.borrowed = borrowed

class Store(ABC):
    @abstractmethod
    def add_book(self, book: Book):
        pass

    @abstractmethod
    def remove_book(self, ident: int):
        pass

    @abstractmethod
    def list_books(self) -> List[Book]:
        pass

    @abstractmethod
    def update_book(self, ident: int, borrowed: Optional[BorrowEvent]):
        pass