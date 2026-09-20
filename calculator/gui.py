import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import messagebox, ttk

from calculator.calculator_engine import (
    Number,
    calculate_expression,
    format_number,
)
from calculator.gui_helpers import (
    append_to_display,
    backspace_display,
    build_history_text,
    format_memory_value,
)
from calculator.storage import (
    History,
    HistoryEntry,
    Memory,
    load_data,
    save_data,
)
from calculator.version import __version__


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root

        self.history: History = []
        self.memory: Memory = {}
        self.last_result: Number | None = None

        self.display_var: tk.StringVar = tk.StringVar()
        self.previous_var: tk.StringVar = tk.StringVar()

        self.load_saved_data()
        self.configure_window()
        self.create_menu()
        self.create_widgets()
        self.create_keyboard_shortcuts()

    def load_saved_data(self) -> None:
        (
            self.history,
            self.memory,
            self.last_result,
        ) = load_data()

    def save(self) -> None:
        try:
            save_data(
                self.history,
                self.memory,
                self.last_result,
            )

        except OSError:
            messagebox.showerror(
                "Error",
                "Calculator data could not be saved.",
            )

    def configure_window(self) -> None:
        self.root.title(f"Simple Scientific Calculator {__version__}")

        self.root.geometry("400x660")
        self.root.resizable(False, False)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_program,
        )

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(
            menu_bar,
            tearoff=False,
        )

        file_menu.add_command(
            label="Clear",
            command=self.clear_display,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.close_program,
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu,
        )

        history_menu = tk.Menu(
            menu_bar,
            tearoff=False,
        )

        history_menu.add_command(
            label="View History",
            command=self.show_history,
        )

        history_menu.add_command(
            label="Clear History",
            command=self.clear_history,
        )

        menu_bar.add_cascade(
            label="History",
            menu=history_menu,
        )

        memory_menu = tk.Menu(
            menu_bar,
            tearoff=False,
        )

        memory_menu.add_command(
            label="Save Last Result",
            command=self.save_last_result_to_memory,
        )

        memory_menu.add_command(
            label="View Memory",
            command=self.show_memory,
        )

        menu_bar.add_cascade(
            label="Memory",
            menu=memory_menu,
        )

        help_menu = tk.Menu(
            menu_bar,
            tearoff=False,
        )

        help_menu.add_command(
            label="About",
            command=self.show_about,
        )

        menu_bar.add_cascade(
            label="Help",
            menu=help_menu,
        )

        self.root.config(
            menu=menu_bar,
        )

    def create_widgets(self) -> None:
        main_frame = ttk.Frame(
            self.root,
            padding=15,
        )

        main_frame.pack(
            fill="both",
            expand=True,
        )

        previous_label = ttk.Label(
            main_frame,
            textvariable=self.previous_var,
            anchor="e",
            font=("Segoe UI", 11),
        )

        previous_label.pack(
            fill="x",
            pady=(0, 2),
        )

        self.display = ttk.Entry(
            main_frame,
            textvariable=self.display_var,
            justify="right",
            font=("Segoe UI", 24),
        )

        self.display.pack(
            fill="x",
            ipady=10,
        )

        tool_frame = ttk.Frame(
            main_frame,
        )

        tool_frame.pack(
            fill="x",
            pady=10,
        )

        ttk.Button(
            tool_frame,
            text="ANS",
            command=self.use_last_result,
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 4),
        )

        ttk.Button(
            tool_frame,
            text="History",
            command=self.show_history,
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=4,
        )

        ttk.Button(
            tool_frame,
            text="Memory",
            command=self.show_memory,
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(4, 0),
        )

        button_frame = ttk.Frame(
            main_frame,
        )

        button_frame.pack(
            fill="both",
            expand=True,
        )

        buttons: list[tuple[str, int, int, int]] = [
            ("C", 0, 0, 1),
            ("⌫", 0, 1, 1),
            ("(", 0, 2, 1),
            (")", 0, 3, 1),
            ("7", 1, 0, 1),
            ("8", 1, 1, 1),
            ("9", 1, 2, 1),
            ("/", 1, 3, 1),
            ("4", 2, 0, 1),
            ("5", 2, 1, 1),
            ("6", 2, 2, 1),
            ("*", 2, 3, 1),
            ("1", 3, 0, 1),
            ("2", 3, 1, 1),
            ("3", 3, 2, 1),
            ("-", 3, 3, 1),
            ("0", 4, 0, 1),
            (".", 4, 1, 1),
            ("%", 4, 2, 1),
            ("+", 4, 3, 1),
            ("//", 5, 0, 1),
            ("**", 5, 1, 1),
            ("=", 5, 2, 2),
        ]

        for text, row, column, columnspan in buttons:
            if text == "C":
                command = self.clear_display

            elif text == "⌫":
                command = self.backspace

            elif text == "=":
                command = self.calculate

            else:
                command = partial(
                    self.button_click,
                    text,
                )

            ttk.Button(
                button_frame,
                text=text,
                command=command,
            ).grid(
                row=row,
                column=column,
                columnspan=columnspan,
                sticky="nsew",
                padx=4,
                pady=4,
            )

        for row in range(6):
            button_frame.rowconfigure(
                row,
                weight=1,
            )

        for column in range(4):
            button_frame.columnconfigure(
                column,
                weight=1,
            )

        self.display.focus_set()

    def button_click(self, value: str) -> None:
        current = self.display_var.get()

        self.display_var.set(
            append_to_display(
                current,
                value,
            )
        )

    def clear_display(self) -> None:
        self.display_var.set("")
        self.previous_var.set("")

    def backspace(self) -> None:
        current = self.display_var.get()

        self.display_var.set(backspace_display(current))

    def calculate(self) -> None:
        expression = self.display_var.get().strip()

        if expression == "":
            return

        try:
            result = calculate_expression(expression)

            formatted_result = format_number(result)

            self.previous_var.set(f"{expression} =")

            self.display_var.set(str(formatted_result))

            self.last_result = result

            history_entry: HistoryEntry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expression": expression,
                "result": result,
            }

            self.history.append(history_entry)

            self.save()

        except ZeroDivisionError:
            messagebox.showerror(
                "Error",
                "Cannot divide by zero.",
            )

        except OverflowError:
            messagebox.showerror(
                "Error",
                "That number is too large.",
            )

        except (
            ValueError,
            SyntaxError,
            TypeError,
        ):
            messagebox.showerror(
                "Error",
                "Invalid calculation.",
            )

    def use_last_result(self) -> None:
        if self.last_result is None:
            messagebox.showinfo(
                "Last Result",
                "No previous result is available.",
            )
            return

        self.button_click(str(format_number(self.last_result)))

    def show_history(self) -> None:
        window = tk.Toplevel(self.root)

        window.title("Calculation History")

        window.geometry("650x400")

        frame = ttk.Frame(
            window,
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Calculation History",
            font=("Segoe UI", 16, "bold"),
        ).pack(
            pady=(0, 10),
        )

        history_box = tk.Text(
            frame,
            font=("Consolas", 11),
            wrap="word",
        )

        history_box.pack(
            fill="both",
            expand=True,
        )

        history_box.insert(
            tk.END,
            build_history_text(self.history),
        )

        history_box.config(
            state="disabled",
        )

        ttk.Button(
            frame,
            text="Clear History",
            command=partial(
                self.clear_history,
                window,
            ),
        ).pack(
            pady=(10, 0),
        )

    def clear_history(
        self,
        window: tk.Toplevel | None = None,
    ) -> None:
        if not self.history:
            messagebox.showinfo(
                "History",
                "History is already empty.",
            )
            return

        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all history?",
        )

        if confirm:
            self.history.clear()
            self.save()

            if window is not None:
                window.destroy()

    def save_last_result_to_memory(self) -> None:
        if self.last_result is None:
            messagebox.showinfo(
                "Memory",
                "There is no result to save.",
            )
            return

        result = self.last_result

        window = tk.Toplevel(self.root)

        window.title("Save to Memory")

        window.geometry("320x170")

        frame = ttk.Frame(
            window,
            padding=15,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Memory name:",
        ).pack(
            anchor="w",
        )

        name_entry = ttk.Entry(frame)

        name_entry.pack(
            fill="x",
            pady=8,
        )

        name_entry.focus_set()

        def save_memory_value() -> None:
            name = name_entry.get().strip()

            if name == "":
                messagebox.showerror(
                    "Error",
                    "Memory name cannot be empty.",
                )
                return

            self.memory[name] = result

            self.save()

            messagebox.showinfo(
                "Memory",
                (f"Saved {name} = {format_number(result)}"),
            )

            window.destroy()

        ttk.Button(
            frame,
            text="Save",
            command=save_memory_value,
        ).pack(
            pady=10,
        )

    def show_memory(self) -> None:
        window = tk.Toplevel(self.root)

        window.title("Saved Memory")

        window.geometry("450x350")

        frame = ttk.Frame(
            window,
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Saved Values",
            font=("Segoe UI", 16, "bold"),
        ).pack(
            pady=(0, 10),
        )

        if not self.memory:
            ttk.Label(
                frame,
                text="No saved values.",
            ).pack(
                pady=20,
            )
            return

        for name, value in self.memory.items():
            row = ttk.Frame(frame)

            row.pack(
                fill="x",
                pady=4,
            )

            ttk.Label(
                row,
                text=format_memory_value(
                    name,
                    value,
                ),
            ).pack(
                side="left",
                fill="x",
                expand=True,
            )

            ttk.Button(
                row,
                text="Use",
                command=partial(
                    self.use_memory_value,
                    value,
                    window,
                ),
            ).pack(
                side="left",
                padx=4,
            )

            ttk.Button(
                row,
                text="Delete",
                command=partial(
                    self.delete_memory_value,
                    name,
                    window,
                ),
            ).pack(
                side="left",
            )

    def use_memory_value(
        self,
        value: Number,
        window: tk.Toplevel,
    ) -> None:
        self.button_click(str(format_number(value)))

        window.destroy()

    def delete_memory_value(
        self,
        name: str,
        window: tk.Toplevel,
    ) -> None:
        if name in self.memory:
            del self.memory[name]

            self.save()

            window.destroy()

            self.show_memory()

    def show_about(self) -> None:
        messagebox.showinfo(
            "About",
            (
                f"Simple Scientific Calculator {__version__}\n\n"
                "Built with Python, tkinter, ttk, JSON, AST, and pytest.\n\n"
                "Features:\n"
                "- Safe expression parsing\n"
                "- Calculation history\n"
                "- Saved memory values\n"
                "- Persistent data storage\n"
                "- Keyboard shortcuts"
            ),
        )

    def create_keyboard_shortcuts(self) -> None:
        self.root.bind(
            "<Key>",
            self.key_pressed,
        )

        self.root.bind(
            "<Control-h>",
            self.show_history_shortcut,
        )

        self.root.bind(
            "<Control-m>",
            self.show_memory_shortcut,
        )

        self.root.bind(
            "<Control-s>",
            self.save_memory_shortcut,
        )

        self.root.bind(
            "<Control-l>",
            self.clear_shortcut,
        )

    def show_history_shortcut(
        self,
        event: tk.Event,
    ) -> None:
        self.show_history()

    def show_memory_shortcut(
        self,
        event: tk.Event,
    ) -> None:
        self.show_memory()

    def save_memory_shortcut(
        self,
        event: tk.Event,
    ) -> None:
        self.save_last_result_to_memory()

    def clear_shortcut(
        self,
        event: tk.Event,
    ) -> None:
        self.clear_display()

    def key_pressed(
        self,
        event: tk.Event,
    ) -> None:
        key = event.keysym
        char = event.char

        if char in "0123456789.+-*/%()":
            self.button_click(char)

        elif key == "Return":
            self.calculate()

        elif key == "BackSpace":
            self.backspace()

        elif key == "Escape":
            self.clear_display()

    def close_program(self) -> None:
        self.save()
        self.root.destroy()
