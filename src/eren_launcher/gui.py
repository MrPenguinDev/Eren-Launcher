from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from .instance_store import InstanceStore


class LauncherGUI:
    """XMCL-inspired desktop UI shell for the launcher."""

    BG = "#131722"
    PANEL = "#1B2333"
    PANEL_ALT = "#222C3E"
    FG = "#E9EEF7"
    MUTED = "#9AA6BD"
    ACCENT = "#6EA8FE"
    SUCCESS = "#39D98A"

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.store = InstanceStore(root_dir)
        self.instances = self.store.list_instances()

    def run(self) -> None:
        app = tk.Tk()
        app.title("Eren Launcher")
        app.geometry("1200x760")
        app.minsize(980, 640)
        app.configure(bg=self.BG)

        style = ttk.Style(app)
        style.theme_use("clam")
        self._configure_styles(style)

        shell = ttk.Frame(app, style="Shell.TFrame")
        shell.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar(shell)
        self._build_main(shell)

        app.mainloop()

    def _configure_styles(self, style: ttk.Style) -> None:
        style.configure("Shell.TFrame", background=self.BG)
        style.configure("Sidebar.TFrame", background=self.PANEL)
        style.configure("Main.TFrame", background=self.BG)
        style.configure("Topbar.TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.PANEL)
        style.configure("CardAlt.TFrame", background=self.PANEL_ALT)
        style.configure("Title.TLabel", background=self.BG, foreground=self.FG, font=("Segoe UI", 22, "bold"))
        style.configure("Section.TLabel", background=self.BG, foreground=self.FG, font=("Segoe UI", 13, "bold"))
        style.configure("Small.TLabel", background=self.PANEL, foreground=self.MUTED, font=("Segoe UI", 9))
        style.configure("CardTitle.TLabel", background=self.PANEL, foreground=self.FG, font=("Segoe UI", 11, "bold"))
        style.configure("CardValue.TLabel", background=self.PANEL, foreground=self.FG, font=("Segoe UI", 18, "bold"))
        style.configure("Sidebar.TButton", background=self.PANEL, foreground=self.FG, borderwidth=0, font=("Segoe UI", 10))
        style.map("Sidebar.TButton", background=[("active", self.PANEL_ALT)])
        style.configure("Accent.TButton", background=self.ACCENT, foreground="#0C1525", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#85B8FF")])

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame", width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="EREN", style="CardValue.TLabel").pack(anchor="w", padx=18, pady=(18, 2))
        ttk.Label(sidebar, text="Launcher", style="Small.TLabel").pack(anchor="w", padx=18, pady=(0, 16))

        for item in [
            "Home",
            "Instances",
            "Mods",
            "Modpacks",
            "Datapacks",
            "Downloads",
            "Diagnostics",
            "Settings",
        ]:
            ttk.Button(sidebar, text=f"  {item}", style="Sidebar.TButton").pack(fill=tk.X, padx=12, pady=3)

        profile = ttk.Frame(sidebar, style="CardAlt.TFrame")
        profile.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=12)
        ttk.Label(profile, text="Signed in: Official Account", style="Small.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(profile, text="Ownership required ✓", foreground=self.SUCCESS, background=self.PANEL_ALT).pack(
            anchor="w", padx=10, pady=(0, 10)
        )

    def _build_main(self, parent: ttk.Frame) -> None:
        main = ttk.Frame(parent, style="Main.TFrame")
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        topbar = ttk.Frame(main, style="Topbar.TFrame")
        topbar.pack(fill=tk.X, padx=18, pady=(16, 10))
        ttk.Label(topbar, text="Home", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Button(topbar, text="Launch Selected", style="Accent.TButton").pack(side=tk.RIGHT)

        cards = ttk.Frame(main, style="Main.TFrame")
        cards.pack(fill=tk.X, padx=18)

        self._metric_card(cards, "Instances", str(len(self.instances)), 0)
        self._metric_card(cards, "Installed Mods", "0", 1)
        self._metric_card(cards, "Queued Downloads", "0", 2)
        self._metric_card(cards, "Java Runtime", "Detected", 3)

        content = ttk.Frame(main, style="Main.TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)

        left = ttk.Frame(content, style="Card.TFrame")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Instances", style="CardTitle.TLabel").pack(anchor="w", padx=12, pady=(12, 6))
        instance_list = tk.Listbox(
            left,
            bg=self.PANEL,
            fg=self.FG,
            highlightthickness=0,
            selectbackground="#31405A",
            relief="flat",
            font=("Segoe UI", 10),
        )
        instance_list.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        if self.instances:
            for name in self.instances:
                instance_list.insert(tk.END, f"{name}   •   Ready")
        else:
            instance_list.insert(tk.END, "No instances yet. Use CLI: create-instance")

        right = ttk.Frame(content, style="CardAlt.TFrame", width=340)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 0))
        right.pack_propagate(False)

        ttk.Label(right, text="Instance Detail", background=self.PANEL_ALT, foreground=self.FG, font=("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=12, pady=(12, 8)
        )
        for line in [
            "Loader matrix: vanilla / fabric / quilt / forge / neoforge",
            "Ownership check: enforced",
            "Logs: structured JSONL",
            "Mod sources: Modrinth + CurseForge",
            "Theme: XMCL-inspired dark",
        ]:
            ttk.Label(right, text=f"• {line}", background=self.PANEL_ALT, foreground=self.MUTED, font=("Segoe UI", 9)).pack(
                anchor="w", padx=12, pady=3
            )

    def _metric_card(self, parent: ttk.Frame, title: str, value: str, column: int) -> None:
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=0, column=column, padx=(0, 12), pady=4, sticky="nsew")
        parent.columnconfigure(column, weight=1)

        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w", padx=12, pady=(10, 3))
        ttk.Label(card, text=value, style="CardValue.TLabel").pack(anchor="w", padx=12, pady=(0, 10))
