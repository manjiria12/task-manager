# 📋 Task Manager — Python Portfolio Project

A fully featured task manager built in **pure Python** — no external libraries.  
Two versions: a polished **CLI app** and a modern **Tkinter GUI app**.

---

## 📁 Project Structure

```
task-manager/
│
├── cli-task-manager/
│   └── main.py          ← CLI version (run this first)
│
├── gui-task-manager/
│   └── gui_app.py       ← GUI version (Tkinter)
│
└── README.md
```

> Both apps save tasks to a `tasks.json` file in the same folder they're run from.

---

## 🚀 How to Run

### CLI Version
```bash
cd cli-task-manager
python main.py
```

### GUI Version
```bash
cd gui-task-manager
python gui_app.py
```

**Requirements:** Python 3.7+  
Tkinter comes built-in with Python on Windows and macOS.  
On Linux: `sudo apt install python3-tk`

---

## ✅ Features

| Feature | CLI | GUI |
|---|:---:|:---:|
| Add task | ✅ | ✅ |
| View all tasks | ✅ | ✅ |
| Mark as done | ✅ | ✅ |
| Delete task | ✅ | ✅ |
| Edit task | ✅ | ✅ |
| Priority (High/Med/Low) | ✅ | ✅ |
| Due date | ✅ | ✅ |
| Notes | ✅ | ✅ |
| JSON persistence | ✅ | ✅ |
| Filter tasks | ✅ | ✅ |
| Search tasks | ❌ | ✅ |
| Statistics | ✅ | ✅ |
| Progress bar | ✅ | ✅ |
| Overdue detection | ✅ | ✅ |
| Colour-coded UI | ✅ | ✅ |

---

## 🧠 Python Concepts Demonstrated

| Concept | Where used |
|---|---|
| **Functions** | Every feature is its own clean function |
| **Dictionaries** | Each task is stored as a `dict` |
| **Lists** | Task collection is a `list` of dicts |
| **File handling** | `json.load()` / `json.dump()` for persistence |
| **Error handling** | `try/except` for invalid input & file errors |
| **f-strings** | Used throughout for formatting |
| **Date/time** | `datetime` module for due dates |
| **OOP (GUI)** | Classes for `TaskApp` and `TaskDialog` |
| **Lambda functions** | Button callbacks in Tkinter |
| **Sorting** | Custom sort key for priority ordering |
| **List comprehensions** | Filtering tasks by status/priority |

---

## 📸 CLI Screenshot

```
╔══════════════════════════════════════╗
║  TASK MANAGER  v1.0                  ║
╠══════════════════════════════════════╣
║  [1]  Add new task                   ║
║  [2]  View all tasks                 ║
║  [3]  Mark task as done              ║
║  [4]  Delete a task                  ║
║  [5]  Edit a task                    ║
║  [6]  Filter tasks                   ║
║  [7]  Statistics                     ║
╠══════════════════════════════════════╣
║  [0]  Exit                           ║
╚══════════════════════════════════════╝
```

---

## 💡 Possible Extensions

- [ ] Export tasks to CSV
- [ ] Task categories / tags
- [ ] Recurring tasks
- [ ] Desktop notifications for due tasks
- [ ] Web version using Flask

---

## 📄 Data Format (tasks.json)

```json
[
  {
    "id": 1,
    "title": "Finish Python project",
    "priority": "high",
    "due": "2025-12-31",
    "note": "Add more features",
    "done": false,
    "created": "2025-04-17 10:30"
  }
]
```
