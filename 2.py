import json
import os
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box

DATA_FILE = "save.json"

console = Console()


# Структуры данных
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


# Менеджер библиотеки
class Library:
    def __init__(self):
        self.books: List[Book] = []
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            self.books = [Book.from_dict(d) for d in data.get("books", [])]
        except Exception as e:
            console.print(f"[red]Ошибка при загрузке файла:[/red] {e}")

    def save(self):
        try:
            data = {"books": [book.to_dict() for book in self.books]}
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            console.print(f"[red]Ошибка при сохранении:[/red] {e}")

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


lib = Library()


# UI helpers
def show_table(books: List[Book], title: str = "Книги"):
    table = Table(title=title, box=box.ROUNDED, show_lines=False)
    table.add_column("Название", style="bold")
    table.add_column("Автор")
    table.add_column("Жанр")
    table.add_column("Год", justify="right")
    table.add_column("Статус", justify="center")
    table.add_column("Избранное", justify="center", no_wrap=True)
    for b in books:
        status = (
            "[green]Прочитана[/green]" if b.read else "[yellow]Не прочитана[/yellow]"
        )
        fav = "★" if b.favorite else ""
        table.add_row( b.title, b.author, b.genre, str(b.year), status, fav)
    console.print(table)


def show_book_detail(b: Book):
    header = Text(f"{b.title}", style="bold magenta")
    meta = f"Автор: {b.author}  |  Жанр: {b.genre}  |  Год: {b.year}"
    status = "Прочитана" if b.read else "Не прочитана"
    fav = "В избранном" if b.favorite else ""
    console.print(
        Panel(
            Text(b.description or "(нет описания)"),
            title=header,
            subtitle=f"{meta} — {status} {fav}",
        )
    )


# Команды
def cmd_add():
    console.print("[bold]Добавление новой книги[/bold]")
    title = Prompt.ask("Название")
    author = Prompt.ask("Автор")
    genre = Prompt.ask("Жанр")
    year = IntPrompt.ask("Год издания")
    description = Prompt.ask("Краткое описание", default="")
    lib.add_book(title, author, genre, year, description)
    lib.save()
    console.print(f"[green]Книга добавлена[/green]")


def cmd_list():
    console.print("[bold]Просмотр книг[/bold]")
    sort_by = Prompt.ask("Сортировка (title/author/year)", default="title")
    genre_filter = Prompt.ask(
        "Фильтр по жанру (оставьте пустым для всех)", default=""
    ).strip()
    genre_filter = genre_filter if genre_filter else None
    status = Prompt.ask("Фильтр по статусу (all/read/unread)", default="all")
    status_filter = None
    if status == "read":
        status_filter = "read"
    elif status == "unread":
        status_filter = "unread"
    books = lib.list_books(
        sort_by=sort_by, genre_filter=genre_filter, status_filter=status_filter
    )
    show_table(books, title="Список книг")
    if books:
        if Confirm.ask("Показать подробности по имени?"):
            book_title = Prompt.ask("Введите имя книги")
            book = lib.find_by_title(book_title)
            if book:
                show_book_detail(book)
            else:
                console.print("[red]Книга с таким именем не найдена[/red]")


def cmd_search():
    console.print("[bold]Поиск книги[/bold]")
    q = Prompt.ask("Введите ключевое слово (в названии, авторе или описании)")
    results = lib.search(q)
    if results:
        show_table(results, title=f"Результаты поиска '{q}'")
    else:
        console.print("[yellow]Ничего не найдено[/yellow]")


def cmd_favorite():
    console.print("[bold]Добавление/Удаление из избранного и смена статуса[/bold]")
    book_title = Prompt.ask("Введите имя книги")
    book = lib.find_by_title(book_title)
    if not book:
        console.print("[red]Книга не найдена[/red]")
        return
    console.print(f"Выбрана: [bold]{book.title}[/bold]")
    if book.read:
        if Confirm.ask("Отметить как не прочитанную?"):
            book.read = False
    else:
        if Confirm.ask("Отметить как прочитанную?"):
            book.read = True
    if book.favorite:
        if Confirm.ask("Удалить из избранного?"):
            book.favorite = False
    else:
        if Confirm.ask("Добавить в избранное?"):
            book.favorite = True

    lib.save()
    console.print("[green]Изменения сохранены[/green]")


def cmd_favorites_list():
    favs = lib.favorites()
    if not favs:
        console.print("[yellow]Нет избранных книг[/yellow]")
        return
    show_table(favs, title="Избранные книги")


def cmd_recommend():
    recs = lib.recommend()
    if not recs:
        console.print(
            "[yellow]Нет рекомендаций — добавьте больше книг или отметьте прочитанные[/yellow]"
        )
    else:
        show_table(recs, title="Рекомендации")
        if Confirm.ask("Добавить рекомендацию в избранное?"):
            book_title = Prompt.ask("Введите имя книги")
            book = lib.find_by_title(book_title)
            if book:
                book.favorite = True
                lib.save()
                console.print("[green]Добавлено в избранное[/green]")
            else:
                console.print("[red]Книга не найдена[/red]")


def cmd_remove():
    console.print("[bold]Удаление книги[/bold]")
    book_title = Prompt.ask("Введите имя книги для удаления")
    book = lib.find_by_title(book_title)
    if not book:
        console.print("[red]Книга не найдена[/red]")
        return
    show_book_detail(book)
    if Confirm.ask("Точно удалить?"):
        ok = lib.remove_book(book_title)
        if ok:
            lib.save()
            console.print("[green]Книга удалена[/green]")
        else:
            console.print("[red]Ошибка при удалении[/red]")


def cmd_quit():
    console.print("[bold]Выход — данные сохранены.[/bold]")
    lib.save()
    raise SystemExit


# Меню
def main_menu():
    menu_table = Table.grid(padding=1)
    menu_table.add_column()
    menu_table.add_column()
    menu_table.add_row("[1] Добавить книгу", "[2] Просмотр книг")
    menu_table.add_row("[3] Поиск книги", "[4] Избранные книги")
    menu_table.add_row("[5] Добавить/изменить статус/избранное", "[6] Рекомендации")
    menu_table.add_row("[7] Удалить книгу", "[0] Выход")
    console.print(
        Panel(
            menu_table,
            title="T-Библиотека",
            subtitle="Выберите действие",
            box=box.DOUBLE,
        )
    )


def main():
    console.clear()
    console.print("[bold magenta]Добро пожаловать в T-Библиотеку[/bold magenta]")
    while True:
        try:
            main_menu()
            choice = Prompt.ask(
                "Введите номер команды",
                choices=[str(i) for i in range(0, 7)],
                default="2",
            )
            if choice == "1":
                cmd_add()
            elif choice == "2":
                cmd_list()
            elif choice == "3":
                cmd_search()
            elif choice == "4":
                cmd_favorites_list()
            elif choice == "5":
                cmd_favorite()
            elif choice == "6":
                cmd_recommend()
            elif choice == "7":
                cmd_remove()
            elif choice == "0":
                cmd_quit()
            else:
                console.print("[red]Неизвестная команда[/red]")
        except KeyboardInterrupt:
            console.print("\n[red]Прерывание: сохранение и выход[/red]")
            lib.save()
            break
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")


if __name__ == "__main__":
    main()
