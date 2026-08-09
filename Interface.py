from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box

from Book import Book
from localization import LANG_EN as t

console = Console()

class LibraryInterface:
    def __init__(self, library):
        self.lib = library

    def error(self, err_msg: str):
        console.print(f"[red]{err_msg}[/red]")

    def greet(self):
        console.clear()
        console.print(f"[bold magenta]{t['welcome']}[/bold magenta]")

    def choose_command(self) -> str:
        return Prompt.ask(
            t["prompt_cmd"],
            choices=[str(i) for i in range(0, 8)],
            default="2",
        )

    def show_table(self, books: List[Book], title: str = None):
        table = Table(title=title or t["title_books"], box=box.ROUNDED, show_lines=False)
        table.add_column(t["col_title"], style="bold")
        table.add_column(t["col_author"])
        table.add_column(t["col_genre"])
        table.add_column(t["col_year"], justify="right")
        table.add_column(t["col_status"], justify="center")
        table.add_column(t["col_fav"], justify="center", no_wrap=True)
        for b in books:
            status = (
                f"[green]{t['status_read']}[/green]" if b.read else f"[yellow]{t['status_unread']}[/yellow]"
            )
            fav = "★" if b.favorite else ""
            table.add_row(b.title, b.author, b.genre, str(b.year), status, fav)
        console.print(table)

    def show_book_detail(self, b: Book):
        header = Text(f"{b.title}", style="bold magenta")
        meta = f"{t['col_author']}: {b.author}  |  {t['col_genre']}: {b.genre}  |  {t['col_year']}: {b.year}"
        status = t["status_read"] if b.read else t["status_unread"]
        fav = t["status_favs"] if b.favorite else ""
        console.print(
            Panel(
                Text(b.description or t["msg_no_desc"]),
                title=header,
                subtitle=f"{meta} — {status} {fav}",
            )
        )

    def cmd_add(self):
        console.print(f"[bold]{t['lbl_add']}[/bold]")
        title = Prompt.ask(t["col_title"])
        author = Prompt.ask(t["col_author"])
        genre = Prompt.ask(t["col_genre"])
        year = IntPrompt.ask(t["col_year"])
        description = Prompt.ask("Description", default="")
        self.lib.add_book(title, author, genre, year, description)
        self.lib.save()
        console.print(f"[green]{t['msg_added_success']}[/green]")

    def cmd_list(self):
        console.print(f"[bold]{t['lbl_browse']}[/bold]")
        sort_by = Prompt.ask("Sort (title/author/year)", default="title")
        genre_filter = Prompt.ask(
            "Filter by genre (leave empty for all)", default=""
        ).strip()
        genre_filter = genre_filter if genre_filter else None
        status = Prompt.ask("Filter by status (all/read/unread)", default="all")
        status_filter = None
        if status == "read":
            status_filter = "read"
        elif status == "unread":
            status_filter = "unread"
        
        books = self.lib.list_books(
            sort_by=sort_by, genre_filter=genre_filter, status_filter=status_filter
        )
        self.show_table(books, title=t["title_list"])
        if books:
            if Confirm.ask(t["q_details"]):
                book_title = Prompt.ask(t["q_title"])
                book = self.lib.find_by_title(book_title)
                if book:
                    self.show_book_detail(book)
                else:
                    console.print(f"[red]{t['err_not_found']}[/red]")

    def cmd_search(self):
        console.print(f"[bold]{t['lbl_search']}[/bold]")
        q = Prompt.ask(t["q_keyword"])
        results = self.lib.search(q)
        if results:
            self.show_table(results, title=f"{t['title_search']} '{q}'")
        else:
            console.print(f"[yellow]{t['err_not_found']}[/yellow]")

    def cmd_favorite(self):
        console.print(f"[bold]{t['lbl_fav_change']}[/bold]")
        book_title = Prompt.ask(t["q_title"])
        book = self.lib.find_by_title(book_title)
        if not book:
            console.print(f"[red]{t['err_not_found']}[/red]")
            return
        console.print(f"{t['lbl_chosen']}: [bold]{book.title}[/bold]")
        if book.read:
            if Confirm.ask(t["q_mark_unread"]):
                book.read = False
        else:
            if Confirm.ask(t["q_mark_read"]):
                book.read = True
        if book.favorite:
            if Confirm.ask(t["q_rem_fav"]):
                book.favorite = False
        else:
            if Confirm.ask(t["q_add_fav"]):
                book.favorite = True

        self.lib.save()
        console.print(f"[green]{t['msg_changes_success']}[/green]")

    def cmd_favorites_list(self):
        favs = self.lib.favorites()
        if not favs:
            console.print(f"[yellow]{t['msg_no_favorites']}[/yellow]")
            return
        self.show_table(favs, title=t["title_favorites"])

    def cmd_recommend(self):
        recs = self.lib.recommend()
        if not recs:
            console.print(f"[yellow]{t['msg_no_recs']}[/yellow]")
        else:
            self.show_table(recs, title=t["title_recs"])
            if Confirm.ask(t["q_add_rec_fav"]):
                book_title = Prompt.ask(t["q_title"])
                book = self.lib.find_by_title(book_title)
                if book:
                    book.favorite = True
                    self.lib.save()
                    console.print(f"[green]{t['msg_changes_success']}[/green]")
                else:
                    console.print(f"[red]{t['err_not_found']}[/red]")

    def cmd_remove(self):
        console.print(f"[bold]{t['lbl_remove']}[/bold]")
        book_title = Prompt.ask(t["q_title_rem"])
        book = self.lib.find_by_title(book_title)
        if not book:
            console.print(f"[red]{t['err_not_found']}[/red]")
            return
        self.show_book_detail(book)
        if Confirm.ask(t["q_confirm_rem"]):
            ok = self.lib.remove_book(book_title)
            if ok:
                self.lib.save()
                console.print(f"[green]{t['msg_removed_success']}[/green]")
            else:
                console.print(f"[red]{t['err_remove']}[/red]")

    def cmd_quit(self):
        console.print(f"[bold]{t['msg_quit']}[/bold]")
        self.lib.save()
        raise SystemExit

    def main_menu(self):
        menu_table = Table.grid(padding=1)
        menu_table.add_column()
        menu_table.add_column()
        menu_table.add_row(t["menu_add"], t["menu_browse"])
        menu_table.add_row(t["menu_search"], t["menu_favs"])
        menu_table.add_row(t["menu_edit"], t["menu_recs"])
        menu_table.add_row(t["menu_remove"], t["menu_exit"])
        console.print(
            Panel(
                menu_table,
                title=t["menu_title"],
                subtitle=t["menu_sub"],
                box=box.DOUBLE,
            )
        )
