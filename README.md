# Smart Library CLI 📚

A lightweight, object-oriented Command Line Interface (CLI) application for managing personal book inventories. It features an interactive Terminal User Interface (TUI) powered by the `rich` library, centralized i18n localization, and local JSON storage for robust data persistence.

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3 (>= 3.9)
* **Package Manager:** `uv` (Fastest toolchain for Python project management)
* **Interface UI:** `rich` (For beautiful terminal text rendering, status bars, and formatted data tables)
* **Data Storage:** JSON (Python Built-in standard library with strict UTF-8 enforcement for safe cyrillic support)
* **Design Patterns:** Object-Oriented Programming (OOP) paired with a clean **MVC-inspired separation of concerns** (Model, View, Dispatcher)
* **Localization:** Extensible dictionary-based i18n architecture

---

## 📂 Project Architecture

The project follows clean code principles and splits execution logic into dedicated modules:
* `library_project/main.py` — The core CLI entry point. It implements a **Dispatch Table (Strategy Pattern)** to handle user routing without cluttered `if-elif` loops.
* `library_project/Library.py` — The business logic engine (Model). Manages state, sorting, searching, and background JSON I/O routines.
* `library_project/Interface.py` — The presentation layer (View). Renders UI components, dynamic data tables, and input forms.
* `library_project/Book.py` — The core data entity. Defines the structural schema and implements type-safe serialization (`to_dict` / `from_dict`).
* `library_project/localization.py` — Centralized localization dictionary isolating client-facing strings from execution code.

---

## 🚀 Getting Started (Using `uv`)

### 1. Installation
Clone the repository and install dependencies using the `uv` package manager:
```bash
uv pip install -e .
```

### 2. Execution
You can run the application directly by targeting the main orchestration script:
```bash
uv run library_project/main.py
```

Alternatively, if installed through `pyproject.toml`, launch the utility globally from anywhere via the generated binary alias:
```bash
smart-library
```

---

## 🧠 Key Features Implemented

1. **Intelligent Book Recommendation Engine:** Automatically calculates and suggests relevant unread books by counting and ranking your most frequently read genres (`collections.Counter`).
2. **Advanced Filtering & Multi-Key Sorting:** Robust sorting routines allowing on-the-fly filtering by specific genres and reading statuses.
3. **Safe Memory Contexts:** Zero global pollution (`global` statements eliminated). State parameters are safely bound inside isolated lexical blocks.
4. **Resilient Process Interruption Handler:** Safely intercepts sudden terminations (`KeyboardInterrupt`) to execute transactional auto-saves to `save.json` before killing the process.
