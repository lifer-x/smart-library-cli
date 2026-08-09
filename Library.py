import os
import json
from typing import List, Optional
from collections import Counter

from Book import Book

class Library:
    def __init__(self, DATA_FILE: str):
        self.books: List[Book] = []
        self.DATA_FILE = DATA_FILE
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book.from_dict(d) for d in data.get("books", [])]
        except Exception as e:
            print(f"Error loading file: {e}")

    def save(self):
        try:
            data = {"books": [book.to_dict() for book in self.books]}
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving file: {e}")

    def add_book(
        self, title: str, author: str, genre: str, year: int, description: str
    ) -> Book:
        book = Book(
            title=title.strip(),
            author=author.strip(),
            genre=genre.strip(),
            year=year,
            description=description.strip(),
        )
        self.books.append(book)
        return book

    def remove_book(self, book_title: str) -> bool:
        initial_count = len(self.books)
        target = book_title.strip().lower()
        self.books = [b for b in self.books if b.title.lower() != target]
        return len(self.books) < initial_count

    def find_by_title(self, book_title: str) -> Optional[Book]:
        target = book_title.strip().lower()
        for book in self.books:
            if book.title.lower() == target:
                return book
        return None

    def search(self, keyword: str) -> List[Book]:
        k = keyword.lower().strip()
        res = []
        for book in self.books:
            if (
                k in book.title.lower()
                or k in book.author.lower()
                or k in book.description.lower()
            ):
                res.append(book)
        return res

    def list_books(
        self,
        sort_by: str = "title",
        genre_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
    ) -> List[Book]:
        res = self.books[:]
        if genre_filter:
            gf = genre_filter.lower().strip()
            res = [b for b in res if b.genre.lower() == gf]
        if status_filter:
            if status_filter == "read":
                res = [b for b in res if b.read]
            elif status_filter == "unread":
                res = [b for b in res if not b.read]
        if sort_by == "title":
            res.sort(key=lambda x: x.title.lower())
        elif sort_by == "author":
            res.sort(key=lambda x: x.author.lower())
        elif sort_by == "year":
            res.sort(key=lambda x: x.year)
        return res

    def favorites(self) -> List[Book]:
        return [b for b in self.books if b.favorite]

    def recommend(self, limit: int = 5) -> List[Book]:
        read_genres = [b.genre for b in self.books if b.read and b.genre]
        if read_genres:
            cnt = Counter([g.lower() for g in read_genres])
            top_genres = [g for g, _ in cnt.most_common(3)]
            rec = [
                b
                for b in self.books
                if (not b.read) and (b.genre.lower() in top_genres)
            ]
            if len(rec) >= limit:
                return rec[:limit]
        rec = [b for b in self.books if not b.read]
        return rec[:limit]
