from typing import Dict
class Book:
    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        year: int,
        description: str,
        read: bool = False,
        favorite: bool = False,
    ):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.read = read
        self.favorite = favorite

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "description": self.description,
            "read": self.read,
            "favorite": self.favorite,
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            title=d.get("title", ""),
            author=d.get("author", ""),
            genre=d.get("genre", ""),
            year=int(d.get("year", 0) or 0),
            description=d.get("description", ""),
            read=bool(d.get("read", False)),
            favorite=bool(d.get("favorite", False)),
        )