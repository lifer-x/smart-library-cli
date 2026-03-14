from Library import Library
from Interface import set_lib,greet, error, choose_command,main_menu,cmd_add,cmd_favorite,cmd_favorites_list,cmd_list,cmd_quit,cmd_recommend,cmd_remove,cmd_search

DATA_FILE = "save.json"

lib = Library(DATA_FILE)
set_lib(lib)

def main():
    greet()
    while True:
        try:
            main_menu()
            choice = choose_command()
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
                error("Неизвестная команда")
        except KeyboardInterrupt:
            error("Прерывание: сохранение и выход")
            lib.save()
            break
        except Exception as e:
            error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
