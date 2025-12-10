from managers.todo_manager import TodoManager
from ui.console_ui import ConsoleUI
from colorama import init, Fore, Style

def main():
    # Initialize colorama
    init(autoreset=True)

    print(Fore.CYAN + Style.BRIGHT + "-----------------------------------------")
    print(Fore.GREEN + Style.BRIGHT + "     🚀 Welcome to Your Todo App CLI")
    print(Fore.CYAN + Style.BRIGHT + "-----------------------------------------")

    todo_manager = TodoManager()
    console_ui = ConsoleUI(todo_manager)
    console_ui.run()

if __name__ == "__main__":
    main()
