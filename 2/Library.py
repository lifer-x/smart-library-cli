import os
import json
from typing import List,Optional

from Book import Book
from Interface import error

class Library:
    def __init__(self,DATA_FILE):
        self.books: List[Book] = []
        self.DATA_FILE = DATA_FILE
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(self.DATA_FILE, "r") as f:
                data = json.load(f)
            self.books = [Book.from_dict(d) for d in data.get("books", [])]
        except Exception as e:
            error(f"Ошибка при загрузке файла: {e}")

    def save(self):
        try:
            data = {"books": [book.to_dict() for book in self.books]}
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            error(f"Ошибка при сохранении: {e}")

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
        for i, book in enumerate(self.books):
            if book.title == book_title:
                del self.books[i]
                return True
        return False

    def find_by_title(self, book_title: str) -> Optional[Book]:
        for book in self.books:
            if book.title == book_title:
                return book
        return None

    def search(self, keyword: str) -> List[Book]:
        k = keyword.lower()
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
            gf = genre_filter.lower()
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
        # простая рекомендация: чаще читаемые жанры -> показываем непрочитанные в тех жанрах,
        # иначе случайные непрочитанные
        from collections import Counter

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
        # fallback: непрочитанные
        rec = [b for b in self.books if not b.read]
        return rec[:limit]