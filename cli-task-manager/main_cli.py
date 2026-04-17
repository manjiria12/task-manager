"""
╔══════════════════════════════════════════════╗
║         CLI TASK MANAGER  v1.0               ║
║   Python · JSON Storage · Priority System    ║
╚══════════════════════════════════════════════╝
"""

import json
import os
import sys
from datetime import datetime, date

# ── File path for saving tasks ──────────────────────────────
DATA_FILE = "tasks.json"

# ── ANSI colour helpers (works on most terminals) ───────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"
    STRIKE = "\033[9m"

def color(text, *codes):
    return "".join(codes) + str(text) + C.RESET


# ── Storage helpers ─────────────────────────────────────────
def load_tasks() -> list:
    """Load tasks from JSON file. Returns empty list if file missing."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(color("  ⚠  Could not read tasks file. Starting fresh.", C.YELLOW))
        return []


def save_tasks(tasks: list) -> None:
    """Persist tasks list to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks: list) -> int:
    """Generate the next unique task ID."""
    return max((t["id"] for t in tasks), default=0) + 1


# ── Display helpers ─────────────────────────────────────────
PRIORITY_STYLES = {
    "high":   (color("● HIGH  ", C.RED,    C.BOLD), C.RED),
    "medium": (color("● MED   ", C.YELLOW, C.BOLD), C.YELLOW),
    "low":    (color("● LOW   ", C.GREEN,  C.BOLD), C.GREEN),
}

def priority_label(p: str):
    label, _ = PRIORITY_STYLES.get(p.lower(), (color("● LOW   ", C.GREEN, C.BOLD), C.GREEN))
    return label

def priority_color(p: str):
    _, clr = PRIORITY_STYLES.get(p.lower(), (None, C.WHITE))
    return clr

def due_label(due_str: str) -> str:
    """Return a coloured due-date label, flagging overdue tasks."""
    if not due_str:
        return color("  no due date  ", C.DIM)
    try:
        due = date.fromisoformat(due_str)
        today = date.today()
        delta = (due - today).days
        if delta < 0:
            return color(f"  OVERDUE {due_str}  ", C.RED, C.BOLD)
        elif delta == 0:
            return color(f"  DUE TODAY       ", C.YELLOW, C.BOLD)
        elif delta <= 3:
            return color(f"  Due {due_str}  ", C.YELLOW)
        else:
            return color(f"  Due {due_str}  ", C.DIM)
    except ValueError:
        return color(f"  {due_str}  ", C.DIM)

def header(title: str) -> None:
    w = 54
    print()
    print(color("─" * w, C.CYAN))
    print(color(f"  {title}", C.CYAN, C.BOLD))
    print(color("─" * w, C.CYAN))

def separator():
    print(color("  " + "·" * 50, C.DIM))

def divider():
    print(color("─" * 54, C.DIM))

def success(msg: str):
    print(color(f"\n  ✓  {msg}", C.GREEN, C.BOLD))

def error(msg: str):
    print(color(f"\n  ✗  {msg}", C.RED))

def info(msg: str):
    print(color(f"\n  ℹ  {msg}", C.CYAN))

def print_task(t: dict, index: int = None) -> None:
    done      = t.get("done", False)
    title     = t["title"]
    priority  = t.get("priority", "low")
    due       = t.get("due", "")
    note      = t.get("note", "")
    created   = t.get("created", "")

    num       = color(f"  #{t['id']:<3}", C.DIM)
    p_label   = priority_label(priority)
    p_clr     = priority_color(priority)

    if done:
        status = color("  ✓  ", C.GREEN, C.BOLD)
        title_str = color(title, C.DIM, C.STRIKE)
    else:
        status = color("  ○  ", C.DIM)
        title_str = color(title, p_clr, C.BOLD)

    print(f"{num} {status} {p_label}  {title_str}")
    if due:
        print(f"       {due_label(due)}")
    if note:
        print(f"       {color('Note: ' + note, C.DIM)}")
    separator()


def print_tasks(tasks: list, show_filter: str = "all") -> None:
    """Print a filtered list of tasks."""
    if show_filter == "pending":
        filtered = [t for t in tasks if not t.get("done")]
        label = "PENDING TASKS"
    elif show_filter == "done":
        filtered = [t for t in tasks if t.get("done")]
        label = "COMPLETED TASKS"
    else:
        filtered = tasks
        label = "ALL TASKS"

    header(label)

    if not filtered:
        print(color("\n  No tasks found.\n", C.DIM))
        return

    # Sort: pending first, then by priority weight
    p_order = {"high": 0, "medium": 1, "low": 2}
    filtered.sort(key=lambda t: (t.get("done", False), p_order.get(t.get("priority", "low"), 2)))

    for t in filtered:
        print_task(t)

    total   = len(tasks)
    pending = sum(1 for t in tasks if not t.get("done"))
    done    = total - pending
    print()
    print(color(f"  Total: {total}  │  Pending: {pending}  │  Done: {done}", C.DIM))
    print()


# ── Core actions ────────────────────────────────────────────
def add_task(tasks: list) -> None:
    header("ADD NEW TASK")

    title = input(color("  Task title  : ", C.WHITE)).strip()
    if not title:
        error("Title cannot be empty.")
        return

    print(color("  Priority    : ", C.WHITE) + "[1] High  [2] Medium  [3] Low  (default: 3)")
    p_choice = input(color("  Choice      : ", C.WHITE)).strip()
    priority = {"1": "high", "2": "medium", "3": "low"}.get(p_choice, "low")

    due = input(color("  Due date    : ", C.WHITE) + color("(YYYY-MM-DD or blank) ", C.DIM)).strip()
    if due:
        try:
            date.fromisoformat(due)
        except ValueError:
            error("Invalid date format. Saving without due date.")
            due = ""

    note = input(color("  Note        : ", C.WHITE) + color("(optional) ", C.DIM)).strip()

    task = {
        "id":       next_id(tasks),
        "title":    title,
        "priority": priority,
        "due":      due,
        "note":     note,
        "done":     False,
        "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    success(f'Task #{task["id"]} "{title}" added  [{priority.upper()}]')


def mark_done(tasks: list) -> None:
    header("MARK TASK AS DONE")
    print_tasks(tasks, "pending")

    pending = [t for t in tasks if not t.get("done")]
    if not pending:
        info("All tasks are already completed!")
        return

    try:
        tid = int(input(color("  Enter task ID to mark as done: ", C.WHITE)).strip())
    except ValueError:
        error("Please enter a valid number.")
        return

    for t in tasks:
        if t["id"] == tid:
            if t["done"]:
                info(f'Task #{tid} is already marked as done.')
                return
            t["done"] = True
            t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            success(f'Task #{tid} "{t["title"]}" marked as complete!')
            return

    error(f"Task #{tid} not found.")


def delete_task(tasks: list) -> None:
    header("DELETE TASK")
    print_tasks(tasks)

    if not tasks:
        return

    try:
        tid = int(input(color("  Enter task ID to delete: ", C.WHITE)).strip())
    except ValueError:
        error("Please enter a valid number.")
        return

    for i, t in enumerate(tasks):
        if t["id"] == tid:
            confirm = input(color(f'  Delete "{t["title"]}"? (y/n): ', C.YELLOW)).strip().lower()
            if confirm == "y":
                tasks.pop(i)
                save_tasks(tasks)
                success(f"Task #{tid} deleted.")
            else:
                info("Deletion cancelled.")
            return

    error(f"Task #{tid} not found.")


def edit_task(tasks: list) -> None:
    header("EDIT TASK")
    print_tasks(tasks)

    if not tasks:
        return

    try:
        tid = int(input(color("  Enter task ID to edit: ", C.WHITE)).strip())
    except ValueError:
        error("Please enter a valid number.")
        return

    for t in tasks:
        if t["id"] == tid:
            print(color(f"\n  Editing Task #{tid} — leave blank to keep current value\n", C.CYAN))

            new_title = input(color(f"  Title    [{t['title']}]: ", C.WHITE)).strip()
            if new_title:
                t["title"] = new_title

            print(color(f"  Priority [{t['priority']}]: ", C.WHITE) + "[1] High  [2] Medium  [3] Low")
            p_choice = input(color("  Choice   : ", C.WHITE)).strip()
            if p_choice in ("1", "2", "3"):
                t["priority"] = {"1": "high", "2": "medium", "3": "low"}[p_choice]

            new_due = input(color(f"  Due date [{t.get('due','none')}] (YYYY-MM-DD): ", C.WHITE)).strip()
            if new_due:
                try:
                    date.fromisoformat(new_due)
                    t["due"] = new_due
                except ValueError:
                    error("Invalid date — keeping previous value.")

            new_note = input(color(f"  Note     [{t.get('note','')}]: ", C.WHITE)).strip()
            if new_note:
                t["note"] = new_note

            save_tasks(tasks)
            success(f'Task #{tid} updated.')
            return

    error(f"Task #{tid} not found.")


def filter_view(tasks: list) -> None:
    header("FILTER TASKS")
    print(color("  [1] All tasks", C.WHITE))
    print(color("  [2] Pending only", C.WHITE))
    print(color("  [3] Completed only", C.WHITE))
    print(color("  [4] High priority only", C.WHITE))

    choice = input(color("\n  Choose filter: ", C.WHITE)).strip()
    if choice == "1":
        print_tasks(tasks, "all")
    elif choice == "2":
        print_tasks(tasks, "pending")
    elif choice == "3":
        print_tasks(tasks, "done")
    elif choice == "4":
        high = [t for t in tasks if t.get("priority") == "high"]
        print_tasks(high, "all")
    else:
        error("Invalid choice.")


def show_stats(tasks: list) -> None:
    header("TASK STATISTICS")
    total   = len(tasks)
    done    = sum(1 for t in tasks if t.get("done"))
    pending = total - done
    high    = sum(1 for t in tasks if t.get("priority") == "high" and not t.get("done"))
    medium  = sum(1 for t in tasks if t.get("priority") == "medium" and not t.get("done"))
    low     = sum(1 for t in tasks if t.get("priority") == "low" and not t.get("done"))
    overdue = 0
    today   = date.today()
    for t in tasks:
        if not t.get("done") and t.get("due"):
            try:
                if date.fromisoformat(t["due"]) < today:
                    overdue += 1
            except ValueError:
                pass

    pct = int((done / total * 100)) if total else 0
    bar_len = 30
    filled  = int(bar_len * pct / 100)
    bar     = color("█" * filled, C.GREEN) + color("░" * (bar_len - filled), C.DIM)

    print(f"\n  Progress   {bar}  {color(str(pct)+'%', C.GREEN, C.BOLD)}")
    print()
    print(f"  {color('Total tasks  :', C.DIM)}  {color(total, C.WHITE, C.BOLD)}")
    print(f"  {color('Completed    :', C.DIM)}  {color(done, C.GREEN, C.BOLD)}")
    print(f"  {color('Pending      :', C.DIM)}  {color(pending, C.YELLOW, C.BOLD)}")
    print(f"  {color('Overdue      :', C.DIM)}  {color(overdue, C.RED, C.BOLD) if overdue else color(0, C.DIM)}")
    print()
    print(f"  Pending by priority:")
    print(f"    {color('HIGH  :', C.RED)}    {high}")
    print(f"    {color('MEDIUM:', C.YELLOW)} {medium}")
    print(f"    {color('LOW   :', C.GREEN)}  {low}")
    print()


# ── Main menu ───────────────────────────────────────────────
def print_menu() -> None:
    print()
    print(color("╔══════════════════════════════════════╗", C.CYAN))
    print(color("║  ", C.CYAN) + color("TASK MANAGER", C.WHITE, C.BOLD) + color("  v1.0           ║", C.CYAN))
    print(color("╠══════════════════════════════════════╣", C.CYAN))
    print(color("║", C.CYAN) + color("  [1]", C.YELLOW) + "  Add new task               " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [2]", C.YELLOW) + "  View all tasks             " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [3]", C.YELLOW) + "  Mark task as done          " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [4]", C.YELLOW) + "  Delete a task              " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [5]", C.YELLOW) + "  Edit a task                " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [6]", C.YELLOW) + "  Filter tasks               " + color("║", C.CYAN))
    print(color("║", C.CYAN) + color("  [7]", C.YELLOW) + "  Statistics                 " + color("║", C.CYAN))
    print(color("╠══════════════════════════════════════╣", C.CYAN))
    print(color("║", C.CYAN) + color("  [0]", C.RED)    + "  Exit                       " + color("║", C.CYAN))
    print(color("╚══════════════════════════════════════╝", C.CYAN))


def main() -> None:
    # Clear screen (cross-platform)
    os.system("cls" if os.name == "nt" else "clear")

    print(color("""
  ╔════════════════════════════════════════╗
  ║                                        ║
  ║       📋  CLI TASK MANAGER  📋         ║
  ║                                        ║
  ║   Add · Track · Prioritise · Done      ║
  ╚════════════════════════════════════════╝
""", C.CYAN))

    tasks = load_tasks()
    pending = sum(1 for t in tasks if not t.get("done"))
    if tasks:
        print(color(f"  Loaded {len(tasks)} task(s)  —  {pending} pending\n", C.DIM))

    actions = {
        "1": add_task,
        "2": lambda t: print_tasks(t, "all"),
        "3": mark_done,
        "4": delete_task,
        "5": edit_task,
        "6": filter_view,
        "7": show_stats,
    }

    while True:
        print_menu()
        choice = input(color("\n  → Enter choice: ", C.WHITE)).strip()

        if choice == "0":
            print(color("\n  Goodbye! Your tasks have been saved. 👋\n", C.GREEN, C.BOLD))
            sys.exit(0)

        action = actions.get(choice)
        if action:
            action(tasks)
        else:
            error("Invalid option. Please choose 0–7.")

        input(color("\n  Press Enter to continue...", C.DIM))
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()