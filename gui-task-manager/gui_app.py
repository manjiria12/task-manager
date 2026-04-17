"""
╔══════════════════════════════════════════════╗
║      TKINTER GUI TASK MANAGER  v2.0          ║
║   Modern GUI · JSON Storage · Priority       ║
╚══════════════════════════════════════════════╝

Run:  python gui_app.py
Requires: Python 3.x  (tkinter is included in standard library)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date

# ── Data file ───────────────────────────────────────────────
DATA_FILE = "tasks.json"

# ── Colour palette ──────────────────────────────────────────
COLORS = {
    "bg":           "#0f0f17",
    "surface":      "#1a1a2e",
    "surface2":     "#16213e",
    "border":       "#2d2d4e",
    "accent":       "#7c6af7",
    "accent_hover": "#9d8fff",
    "text":         "#e8e8f0",
    "text_dim":     "#8888aa",
    "success":      "#43e97b",
    "danger":       "#ff6b6b",
    "warn":         "#f9a825",
    "high":         "#ff6b6b",
    "medium":       "#f9a825",
    "low":          "#43e97b",
    "done_bg":      "#1a2a1a",
    "done_fg":      "#446644",
    "selected":     "#2d2860",
}

FONTS = {
    "title":   ("Segoe UI", 22, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "body":    ("Segoe UI", 11),
    "small":   ("Segoe UI", 9),
    "mono":    ("Consolas", 10),
    "tag":     ("Segoe UI", 9, "bold"),
}

# ── Storage ─────────────────────────────────────────────────
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


# ── Add / Edit Dialog ────────────────────────────────────────
class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task=None):
        super().__init__(parent)
        self.result = None
        self.task = task
        is_edit = task is not None

        self.title("Edit Task" if is_edit else "Add New Task")
        self.configure(bg=COLORS["surface"])
        self.resizable(False, False)
        self.grab_set()

        # Center on parent
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        w, h = 460, 420
        self.geometry(f"{w}x{h}+{px + pw//2 - w//2}+{py + ph//2 - h//2}")

        self._build(is_edit)
        if is_edit:
            self._populate(task)

        self.wait_window()

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, bg=COLORS["surface"], fg=COLORS["text_dim"],
                 font=FONTS["small"]).pack(anchor="w", padx=20, pady=(10, 2))

    def _entry(self, parent, textvariable=None, **kw):
        e = tk.Entry(parent, textvariable=textvariable,
                     bg=COLORS["surface2"], fg=COLORS["text"],
                     insertbackground=COLORS["text"],
                     relief="flat", bd=0,
                     font=FONTS["body"],
                     highlightthickness=1,
                     highlightbackground=COLORS["border"],
                     highlightcolor=COLORS["accent"],
                     **kw)
        e.pack(fill="x", padx=20, ipady=6)
        return e

    def _build(self, is_edit):
        # Header
        hdr = tk.Frame(self, bg=COLORS["accent"], height=4)
        hdr.pack(fill="x")

        tk.Label(self, text="Edit Task" if is_edit else "✚  New Task",
                 bg=COLORS["surface"], fg=COLORS["text"],
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(16, 4))

        # Title
        self._lbl(self, "Task title *")
        self.title_var = tk.StringVar()
        self._entry(self, textvariable=self.title_var)

        # Note
        self._lbl(self, "Note (optional)")
        self.note_var = tk.StringVar()
        self._entry(self, textvariable=self.note_var)

        # Priority + Due date row
        row = tk.Frame(self, bg=COLORS["surface"])
        row.pack(fill="x", padx=20, pady=(10, 0))

        # Priority
        p_frame = tk.Frame(row, bg=COLORS["surface"])
        p_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(p_frame, text="Priority", bg=COLORS["surface"],
                 fg=COLORS["text_dim"], font=FONTS["small"]).pack(anchor="w")
        self.priority_var = tk.StringVar(value="medium")
        combo_style = ttk.Style()
        combo_style.theme_use("clam")
        combo_style.configure("TCombobox",
                              fieldbackground=COLORS["surface2"],
                              background=COLORS["surface2"],
                              foreground=COLORS["text"],
                              selectbackground=COLORS["selected"],
                              selectforeground=COLORS["text"],
                              bordercolor=COLORS["border"],
                              arrowcolor=COLORS["text_dim"])
        self.prio_combo = ttk.Combobox(p_frame, textvariable=self.priority_var,
                                       values=["high", "medium", "low"],
                                       state="readonly", width=12)
        self.prio_combo.pack(fill="x", ipady=4)

        # Due date
        d_frame = tk.Frame(row, bg=COLORS["surface"])
        d_frame.pack(side="left", fill="x", expand=True)
        tk.Label(d_frame, text="Due date (YYYY-MM-DD)", bg=COLORS["surface"],
                 fg=COLORS["text_dim"], font=FONTS["small"]).pack(anchor="w")
        self.due_var = tk.StringVar()
        tk.Entry(d_frame, textvariable=self.due_var,
                 bg=COLORS["surface2"], fg=COLORS["text"],
                 insertbackground=COLORS["text"],
                 relief="flat", bd=0, font=FONTS["body"],
                 highlightthickness=1,
                 highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["accent"],
                 width=16).pack(fill="x", ipady=6)

        # Buttons
        btn_row = tk.Frame(self, bg=COLORS["surface"])
        btn_row.pack(fill="x", padx=20, pady=20, side="bottom")

        cancel_btn = tk.Button(btn_row, text="Cancel",
                               bg=COLORS["surface2"], fg=COLORS["text_dim"],
                               activebackground=COLORS["border"],
                               activeforeground=COLORS["text"],
                               relief="flat", font=FONTS["body"],
                               padx=20, pady=8, cursor="hand2",
                               command=self.destroy)
        cancel_btn.pack(side="right", padx=(6, 0))

        save_btn = tk.Button(btn_row,
                             text="Save Changes" if is_edit else "Add Task",
                             bg=COLORS["accent"], fg="#fff",
                             activebackground=COLORS["accent_hover"],
                             activeforeground="#fff",
                             relief="flat", font=("Segoe UI", 11, "bold"),
                             padx=20, pady=8, cursor="hand2",
                             command=self._submit)
        save_btn.pack(side="right")

    def _populate(self, task):
        self.title_var.set(task.get("title", ""))
        self.note_var.set(task.get("note", ""))
        self.priority_var.set(task.get("priority", "medium"))
        self.due_var.set(task.get("due", ""))

    def _submit(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Missing Title", "Task title cannot be empty.", parent=self)
            return
        due = self.due_var.get().strip()
        if due:
            try:
                date.fromisoformat(due)
            except ValueError:
                messagebox.showwarning("Invalid Date",
                    "Date must be YYYY-MM-DD format.\nExample: 2025-12-31", parent=self)
                return
        self.result = {
            "title":    title,
            "note":     self.note_var.get().strip(),
            "priority": self.priority_var.get(),
            "due":      due,
        }
        self.destroy()


# ── Main Application ─────────────────────────────────────────
class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.configure(bg=COLORS["bg"])
        self.minsize(820, 560)
        self.geometry("960x640")

        # Try to set a nice icon / title bar colour on Windows
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self.tasks = load_tasks()
        self.filter_mode = tk.StringVar(value="all")
        self.search_var  = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh())

        self._build_ui()
        self._refresh()

    # ── UI Construction ──────────────────────────────────────
    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────
        sidebar = tk.Frame(self, bg=COLORS["surface"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # App title
        tk.Label(sidebar, text="📋", bg=COLORS["surface"],
                 font=("Segoe UI", 28)).pack(pady=(28, 4))
        tk.Label(sidebar, text="Task Manager", bg=COLORS["surface"],
                 fg=COLORS["text"], font=("Segoe UI", 13, "bold")).pack()
        tk.Label(sidebar, text="v2.0", bg=COLORS["surface"],
                 fg=COLORS["text_dim"], font=FONTS["small"]).pack(pady=(0, 24))

        # Filter buttons
        filters = [
            ("All Tasks",    "all"),
            ("⏳  Pending",   "pending"),
            ("✅  Completed", "done"),
            ("🔴  High Prio", "high"),
        ]
        self._filter_btns = {}
        for label, val in filters:
            btn = tk.Button(sidebar, text=label,
                            bg=COLORS["surface"], fg=COLORS["text"],
                            activebackground=COLORS["selected"],
                            activeforeground=COLORS["text"],
                            relief="flat", font=FONTS["body"],
                            anchor="w", padx=20, pady=8, cursor="hand2",
                            command=lambda v=val: self._set_filter(v))
            btn.pack(fill="x")
            self._filter_btns[val] = btn

        # Stats panel
        self.stats_frame = tk.Frame(sidebar, bg=COLORS["surface"])
        self.stats_frame.pack(fill="x", padx=16, pady=(24, 0))

        # Bottom: Add button
        add_btn = tk.Button(sidebar, text="＋  Add Task",
                            bg=COLORS["accent"], fg="#fff",
                            activebackground=COLORS["accent_hover"],
                            activeforeground="#fff",
                            relief="flat",
                            font=("Segoe UI", 11, "bold"),
                            pady=12, cursor="hand2",
                            command=self._add_task)
        add_btn.pack(fill="x", padx=16, pady=16, side="bottom")

        # ── Main area ────────────────────────────────────────
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(side="left", fill="both", expand=True)

        # Topbar
        topbar = tk.Frame(main, bg=COLORS["surface"], height=56)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.view_title = tk.Label(topbar, text="All Tasks",
                                   bg=COLORS["surface"], fg=COLORS["text"],
                                   font=("Segoe UI", 13, "bold"))
        self.view_title.pack(side="left", padx=20)

        # Search bar
        search_frame = tk.Frame(topbar, bg=COLORS["surface2"],
                                 highlightthickness=1,
                                 highlightbackground=COLORS["border"],
                                 highlightcolor=COLORS["accent"])
        search_frame.pack(side="right", padx=16, pady=10)
        tk.Label(search_frame, text="🔍", bg=COLORS["surface2"],
                 fg=COLORS["text_dim"], font=("Segoe UI", 10)).pack(side="left", padx=(8, 0))
        tk.Entry(search_frame, textvariable=self.search_var,
                 bg=COLORS["surface2"], fg=COLORS["text"],
                 insertbackground=COLORS["text"],
                 relief="flat", bd=0, width=22,
                 font=FONTS["body"]).pack(side="left", padx=6, pady=5)

        # Task list (canvas + scrollbar)
        list_frame = tk.Frame(main, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.canvas = tk.Canvas(list_frame, bg=COLORS["bg"],
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                  command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.task_container = tk.Frame(self.canvas, bg=COLORS["bg"])
        self._canvas_window = self.canvas.create_window(
            (0, 0), window=self.task_container, anchor="nw")

        self.task_container.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self._canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    # ── Stats panel ──────────────────────────────────────────
    def _update_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        total   = len(self.tasks)
        done    = sum(1 for t in self.tasks if t.get("done"))
        pending = total - done
        pct     = int(done / total * 100) if total else 0

        def stat_row(label, val, color):
            row = tk.Frame(self.stats_frame, bg=COLORS["surface"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, bg=COLORS["surface"],
                     fg=COLORS["text_dim"], font=FONTS["small"]).pack(side="left")
            tk.Label(row, text=str(val), bg=COLORS["surface"],
                     fg=color, font=("Segoe UI", 10, "bold")).pack(side="right")

        stat_row("Total",     total,   COLORS["text"])
        stat_row("Pending",   pending, COLORS["warn"])
        stat_row("Done",      done,    COLORS["success"])

        # Progress bar
        tk.Label(self.stats_frame, text=f"Progress  {pct}%",
                 bg=COLORS["surface"], fg=COLORS["text_dim"],
                 font=FONTS["small"]).pack(anchor="w", pady=(10, 2))
        bar_bg = tk.Frame(self.stats_frame, bg=COLORS["border"],
                          height=6, bd=0)
        bar_bg.pack(fill="x")
        if pct > 0:
            bar_fill = tk.Frame(bar_bg, bg=COLORS["success"], height=6)
            bar_fill.place(relwidth=pct/100, relheight=1)

    # ── Filter ───────────────────────────────────────────────
    def _set_filter(self, val):
        self.filter_mode.set(val)
        labels = {"all":"All Tasks","pending":"Pending","done":"Completed","high":"High Priority"}
        self.view_title.config(text=labels.get(val,"All Tasks"))
        for k, btn in self._filter_btns.items():
            btn.config(bg=COLORS["selected"] if k == val else COLORS["surface"],
                       fg=COLORS["text"])
        self._refresh()

    # ── Task Card ────────────────────────────────────────────
    def _make_card(self, parent, task):
        done     = task.get("done", False)
        priority = task.get("priority", "low")
        due      = task.get("due", "")
        note     = task.get("note", "")

        prio_color = {"high": COLORS["high"], "medium": COLORS["warn"],
                      "low": COLORS["low"]}.get(priority, COLORS["low"])

        card_bg = COLORS["done_bg"] if done else COLORS["surface"]

        card = tk.Frame(parent, bg=card_bg, cursor="arrow",
                        highlightthickness=1,
                        highlightbackground=COLORS["border"] if not done else COLORS["border"])
        card.pack(fill="x", padx=16, pady=4)

        # Left priority stripe
        stripe = tk.Frame(card, bg=prio_color if not done else COLORS["border"], width=4)
        stripe.pack(side="left", fill="y")

        body = tk.Frame(card, bg=card_bg)
        body.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        # Row 1: title + done checkbox
        row1 = tk.Frame(body, bg=card_bg)
        row1.pack(fill="x")

        # Done toggle button
        done_btn = tk.Button(row1,
                             text="✓" if done else "○",
                             bg=COLORS["success"] if done else card_bg,
                             fg="#fff" if done else COLORS["text_dim"],
                             activebackground=COLORS["success"],
                             activeforeground="#fff",
                             relief="flat", font=("Segoe UI", 11, "bold"),
                             width=2, cursor="hand2",
                             command=lambda t=task: self._toggle_done(t))
        done_btn.pack(side="left", padx=(0, 8))

        title_fg = COLORS["done_fg"] if done else COLORS["text"]
        title_font = ("Segoe UI", 11) if done else ("Segoe UI", 11, "bold")
        tk.Label(row1, text=task["title"], bg=card_bg, fg=title_fg,
                 font=title_font).pack(side="left")

        # Priority badge
        p_text = priority.upper()
        p_bg = {
            "high":   "#3a1a1a", "medium": "#3a2a00", "low": "#0a2a1a"
        }.get(priority, "#0a2a1a")
        tk.Label(row1, text=p_text, bg=p_bg, fg=prio_color,
                 font=FONTS["tag"], padx=6, pady=1).pack(side="left", padx=8)

        # Row 2: meta info
        meta = []
        if due:
            try:
                due_d = date.fromisoformat(due)
                today = date.today()
                delta = (due_d - today).days
                if done:
                    meta.append(("📅 " + due, COLORS["text_dim"]))
                elif delta < 0:
                    meta.append(("⚠ OVERDUE: " + due, COLORS["high"]))
                elif delta == 0:
                    meta.append(("⏰ Due today", COLORS["warn"]))
                else:
                    meta.append(("📅 Due " + due, COLORS["text_dim"]))
            except ValueError:
                meta.append(("📅 " + due, COLORS["text_dim"]))
        if note:
            meta.append(("💬 " + note, COLORS["text_dim"]))
        if task.get("completed_at"):
            meta.append(("✓ Completed " + task["completed_at"], COLORS["success"]))

        if meta:
            row2 = tk.Frame(body, bg=card_bg)
            row2.pack(fill="x", pady=(4, 0))
            for txt, fg in meta:
                tk.Label(row2, text=txt, bg=card_bg, fg=fg,
                         font=FONTS["small"]).pack(side="left", padx=(0, 16))

        # Action buttons (right side)
        actions = tk.Frame(card, bg=card_bg)
        actions.pack(side="right", padx=8)

        edit_btn = tk.Button(actions, text="✏", bg=card_bg, fg=COLORS["text_dim"],
                             activebackground=COLORS["border"],
                             activeforeground=COLORS["text"],
                             relief="flat", font=("Segoe UI", 12),
                             cursor="hand2", padx=6,
                             command=lambda t=task: self._edit_task(t))
        edit_btn.pack(side="left")

        del_btn = tk.Button(actions, text="🗑", bg=card_bg, fg=COLORS["text_dim"],
                            activebackground="#3a1a1a",
                            activeforeground=COLORS["high"],
                            relief="flat", font=("Segoe UI", 12),
                            cursor="hand2", padx=6,
                            command=lambda t=task: self._delete_task(t))
        del_btn.pack(side="left")

    # ── Refresh view ─────────────────────────────────────────
    def _refresh(self):
        for w in self.task_container.winfo_children():
            w.destroy()

        f = self.filter_mode.get()
        q = self.search_var.get().strip().lower()

        if f == "pending":
            filtered = [t for t in self.tasks if not t.get("done")]
        elif f == "done":
            filtered = [t for t in self.tasks if t.get("done")]
        elif f == "high":
            filtered = [t for t in self.tasks if t.get("priority") == "high" and not t.get("done")]
        else:
            filtered = list(self.tasks)

        if q:
            filtered = [t for t in filtered
                        if q in t["title"].lower() or q in t.get("note","").lower()]

        # Sort: pending first, then priority
        p_ord = {"high": 0, "medium": 1, "low": 2}
        filtered.sort(key=lambda t: (t.get("done", False),
                                     p_ord.get(t.get("priority","low"), 2)))

        if not filtered:
            msg = "No tasks found."
            if q:
                msg = f'No results for "{q}"'
            tk.Label(self.task_container, text=msg,
                     bg=COLORS["bg"], fg=COLORS["text_dim"],
                     font=("Segoe UI", 13)).pack(pady=48)
        else:
            for t in filtered:
                self._make_card(self.task_container, t)

        self._update_stats()
        self._highlight_filter()

    def _highlight_filter(self):
        val = self.filter_mode.get()
        for k, btn in self._filter_btns.items():
            btn.config(bg=COLORS["selected"] if k == val else COLORS["surface"])

    # ── Actions ──────────────────────────────────────────────
    def _add_task(self):
        dlg = TaskDialog(self)
        if dlg.result:
            task = {
                "id":       next_id(self.tasks),
                "done":     False,
                "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                **dlg.result,
            }
            self.tasks.append(task)
            save_tasks(self.tasks)
            self._refresh()

    def _edit_task(self, task):
        dlg = TaskDialog(self, task=task)
        if dlg.result:
            task.update(dlg.result)
            save_tasks(self.tasks)
            self._refresh()

    def _toggle_done(self, task):
        task["done"] = not task["done"]
        if task["done"]:
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        else:
            task.pop("completed_at", None)
        save_tasks(self.tasks)
        self._refresh()

    def _delete_task(self, task):
        if messagebox.askyesno("Delete Task",
                               f"Delete \"{task['title']}\"?\nThis cannot be undone.",
                               icon="warning"):
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self._refresh()


# ── Entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()