# TODO_APP_CLI

📝 TodoApp CLI

A simple, fast, and colorful command-line Todo Application built in Python, following spec-driven development using Claude Code + Spec-Kit Plus.

This is Phase I of the project and includes all Basic Level features:
✔ Add tasks
✔ View tasks
✔ Update tasks
✔ Delete tasks
✔ Mark complete / incomplete
✔ In-memory storage
✔ Clean project structure
✔ Colorful UI powered by Rich 🌈

🚀 Features
✅ Core Functionality

Add a new task with title and optional description

List all tasks with status icons (✓ completed / ○ pending)

Edit a task (title or description)

Delete a task by ID

Mark as complete / incomplete

Automatically track created & updated timestamps

🎨 UI Enhancements

Beautiful colored terminal output using Rich

Clear menus

Stylish headings

Clean logs and separators

Emoji support for better user experience

📁 Project Structure
todoapp/
│── src/
│   ├── managers/
│   │   └── todo_manager.py
│   ├── models/
│   │   └── task.py
│   ├── ui/
│   │   └── console_ui.py
│   ├── main.py
│
│── specs-history/     # All spec files
│── constitution.md     # Claude Code Constitution
│── CLAUDE.md           # Claude usage instructions
│── README.md

⚙️ Installation & Setup
✔ Prerequisites

Python 3.13+

UV package manager

WSL 2 (Windows users)

🐧 Windows Users – Enable WSL2
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04


Reboot your system after installation.

📦 Setup Project

Clone the repository:

git clone https://github.com/yourusername/todoapp-cli.git
cd todoapp-cli


Install dependencies using uv:

uv sync


Or using pip:

pip install rich

▶️ Run the App
python3 src/main.py


You’ll see the colorful menu:

===== MY TODO APP =====
1. Add New Task
2. Show All Tasks
3. Edit Task
4. Delete Task
5. Mark Task Done
6. Mark Task Not Done
7. Exit Program
========================

📘 Example Output
📋 Things to do:
[○] 1: Finish Python Project

✅ Completed tasks:
[✓] 2: Buy Groceries

🛠 Tech Stack

Python 3.13

Rich (for colored output)

Spec-Kit Plus

Claude Code

UV package manager

WSL2 for Windows Development

🤖 Spec-Driven Development

This project was developed using:

constitution file

spec history folder

iterative specs

automated implementation with Claude Code

💡 Future Improvements (Phase II)

File-based persistence

JSON / SQLite storage

Search / filter tasks

Priority levels

Deadlines & reminders

Export tasks

👩‍💻 Author

Faqeha Noor
Student • Developer • Tech Enthusiast

