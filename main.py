from Library import Library
from Interface import LibraryInterface
from localization import LANG_EN as t

DATA_FILE = "save.json"


def main():
    lib = Library(DATA_FILE)
    ui = LibraryInterface(lib)

    commands = {
        "1": ui.cmd_add,
        "2": ui.cmd_list,
        "3": ui.cmd_search,
        "4": ui.cmd_favorites_list,
        "5": ui.cmd_favorite,
        "6": ui.cmd_recommend,
        "7": ui.cmd_remove,
        "0": ui.cmd_quit,
    }

    ui.greet()

    while True:
        try:
            ui.main_menu()
            choice = ui.choose_command()

            if choice in commands:
                commands[choice]()
            else:
                ui.error(t["err_unknown"])

        except KeyboardInterrupt:
            ui.error(t["msg_interrupted"])
            lib.save()
            break
        except Exception as e:
            ui.error(f"{t['err_occurred']}: {e}")


if __name__ == "__main__":
    main()
