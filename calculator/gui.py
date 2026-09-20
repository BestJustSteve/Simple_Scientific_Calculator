import tkinter as tk
from collections.abc import Callable
from datetime import datetime
from functools import partial
from tkinter import messagebox, ttk

from calculator.calculator_engine import (
    AngleMode,
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
        self.just_calculated: bool = False

        self.display_var: tk.StringVar = tk.StringVar()
        self.previous_var: tk.StringVar = tk.StringVar()
        self.angle_mode_var: tk.StringVar = tk.StringVar(value="radians")
        self.mode_status_var: tk.StringVar = tk.StringVar(value="RAD")

        self.load_saved_data()
        self.configure_window()
        self.configure_styles()
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

    def center_window(
        self,
        window: tk.Tk | tk.Toplevel,
        width: int,
        height: int,
    ) -> None:
        window.update_idletasks()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = max(
            0,
            (screen_width - width) // 2,
        )
        y = max(
            0,
            (screen_height - height) // 2,
        )

        window.geometry(f"{width}x{height}+{x}+{y}")

    def center_child_window(
        self,
        window: tk.Toplevel,
        width: int,
        height: int,
    ) -> None:
        self.root.update_idletasks()
        window.update_idletasks()

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        x = root_x + max(
            0,
            (root_width - width) // 2,
        )
        y = root_y + max(
            0,
            (root_height - height) // 2,
        )

        window.geometry(f"{width}x{height}+{x}+{y}")

    def configure_window(self) -> None:
        self.root.title(f"Simple Scientific Calculator {__version__}")

        self.center_window(
            self.root,
            560,
            790,
        )

        self.root.minsize(
            560,
            790,
        )

        self.root.resizable(
            True,
            True,
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_program,
        )

    def configure_styles(self) -> None:
        style = ttk.Style(self.root)

        style.configure(
            "Display.TEntry",
            font=(
                "Segoe UI",
                24,
            ),
            padding=12,
        )

        style.configure(
            "Calculator.TButton",
            font=(
                "Segoe UI",
                12,
            ),
            padding=8,
        )

        style.configure(
            "Scientific.TButton",
            font=(
                "Segoe UI",
                10,
            ),
            padding=6,
        )

        style.configure(
            "Tool.TButton",
            font=(
                "Segoe UI",
                10,
            ),
            padding=6,
        )

        style.configure(
            "Section.TLabelframe.Label",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
        )

        style.configure(
            "Status.TLabel",
            font=(
                "Segoe UI",
                9,
            ),
            padding=4,
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

        help_menu = tk.Menu(
            menu_bar,
            tearoff=False,
        )
        help_menu.add_command(
            label="Keyboard Shortcuts",
            command=self.show_keyboard_shortcuts,
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="About",
            command=self.show_about,
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu,
        )
        menu_bar.add_cascade(
            label="History",
            menu=history_menu,
        )
        menu_bar.add_cascade(
            label="Memory",
            menu=memory_menu,
        )
        menu_bar.add_cascade(
            label="Help",
            menu=help_menu,
        )

        self.root.config(menu=menu_bar)

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
            style="Display.TEntry",
            state="readonly",
        )
        self.display.pack(
            fill="x",
            ipady=10,
        )

        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(
            fill="x",
            pady=(8, 8),
        )

        ttk.Label(
            mode_frame,
            text="Angle Mode:",
        ).pack(side="left")

        ttk.Radiobutton(
            mode_frame,
            text="DEG",
            variable=self.angle_mode_var,
            value="degrees",
            command=self.update_mode_status,
        ).pack(
            side="left",
            padx=(10, 4),
        )

        ttk.Radiobutton(
            mode_frame,
            text="RAD",
            variable=self.angle_mode_var,
            value="radians",
            command=self.update_mode_status,
        ).pack(
            side="left",
            padx=4,
        )

        tool_frame = ttk.Frame(main_frame)
        tool_frame.pack(
            fill="x",
            pady=(0, 8),
        )

        ttk.Button(
            tool_frame,
            text="ANS",
            style="Tool.TButton",
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
            style="Tool.TButton",
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
            style="Tool.TButton",
            command=self.show_memory,
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(4, 0),
        )

        scientific_frame = ttk.LabelFrame(
            main_frame,
            text="Scientific",
            padding=8,
            style="Section.TLabelframe",
        )
        scientific_frame.pack(
            fill="x",
            pady=(0, 10),
        )

        scientific_buttons: list[tuple[str, str, int, int, bool]] = [
            ("sin", "sin(", 0, 0, False),
            ("cos", "cos(", 0, 1, False),
            ("tan", "tan(", 0, 2, False),
            ("asin", "asin(", 0, 3, False),
            ("acos", "acos(", 0, 4, False),
            ("atan", "atan(", 0, 5, False),
            ("√", "sqrt", 1, 0, True),
            ("x²", "square", 1, 1, True),
            ("1/x", "reciprocal", 1, 2, True),
            ("n!", "factorial", 1, 3, True),
            ("log", "log", 1, 4, True),
            ("ln", "ln", 1, 5, True),
            ("10ˣ", "pow10", 2, 0, True),
            ("eˣ", "exp", 2, 1, True),
            ("π", "pi", 2, 2, False),
            ("e", "e", 2, 3, False),
            ("(", "(", 2, 4, False),
            (")", ")", 2, 5, False),
        ]

        for (
            label,
            value,
            row,
            column,
            apply_current,
        ) in scientific_buttons:
            scientific_command: Callable[[], None]

            if apply_current:
                scientific_command = partial(
                    self.apply_to_current_expression,
                    value,
                )
            else:
                scientific_command = partial(
                    self.button_click,
                    value,
                )

            ttk.Button(
                scientific_frame,
                text=label,
                style="Scientific.TButton",
                command=scientific_command,
            ).grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=3,
                pady=3,
                ipady=3,
            )

        for column in range(6):
            scientific_frame.columnconfigure(
                column,
                weight=1,
            )

        calculator_frame = ttk.LabelFrame(
            main_frame,
            text="Calculator",
            padding=8,
            style="Section.TLabelframe",
        )
        calculator_frame.pack(
            fill="both",
            expand=True,
        )

        buttons: list[tuple[str, int, int, int]] = [
            ("C", 0, 0, 1),
            ("⌫", 0, 1, 1),
            ("%", 0, 2, 1),
            ("/", 0, 3, 1),
            ("7", 1, 0, 1),
            ("8", 1, 1, 1),
            ("9", 1, 2, 1),
            ("*", 1, 3, 1),
            ("4", 2, 0, 1),
            ("5", 2, 1, 1),
            ("6", 2, 2, 1),
            ("-", 2, 3, 1),
            ("1", 3, 0, 1),
            ("2", 3, 1, 1),
            ("3", 3, 2, 1),
            ("+", 3, 3, 1),
            ("0", 4, 0, 1),
            (".", 4, 1, 1),
            ("//", 4, 2, 1),
            ("**", 4, 3, 1),
            ("=", 5, 0, 4),
        ]

        for (
            text,
            row,
            column,
            columnspan,
        ) in buttons:
            calculator_command: Callable[[], None]

            if text == "C":
                calculator_command = self.clear_display
            elif text == "⌫":
                calculator_command = self.backspace
            elif text == "=":
                calculator_command = self.calculate
            else:
                calculator_command = partial(
                    self.button_click,
                    text,
                )

            ttk.Button(
                calculator_frame,
                text=text,
                style="Calculator.TButton",
                command=calculator_command,
            ).grid(
                row=row,
                column=column,
                columnspan=columnspan,
                sticky="nsew",
                padx=4,
                pady=4,
                ipady=4,
            )

        for row in range(6):
            calculator_frame.rowconfigure(
                row,
                weight=1,
            )

        for column in range(4):
            calculator_frame.columnconfigure(
                column,
                weight=1,
            )

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(
            fill="x",
            pady=(8, 0),
        )

        ttk.Label(
            status_frame,
            text="Angle:",
            style="Status.TLabel",
        ).pack(side="left")

        ttk.Label(
            status_frame,
            textvariable=self.mode_status_var,
            style="Status.TLabel",
        ).pack(side="left")

        ttk.Label(
            status_frame,
            text="F1: Keyboard Shortcuts",
            style="Status.TLabel",
        ).pack(side="right")

        self.display.focus_set()

    def is_operator(
        self,
        value: str,
    ) -> bool:
        return value in {
            "+",
            "-",
            "*",
            "/",
            "%",
            "//",
            "**",
        }

    def is_constant(
        self,
        value: str,
    ) -> bool:
        return value in {
            "pi",
            "e",
        }

    def is_function_prefix(
        self,
        value: str,
    ) -> bool:
        return value in {
            "sin(",
            "cos(",
            "tan(",
            "asin(",
            "acos(",
            "atan(",
        }

    def expression_ends_with_constant(
        self,
        expression: str,
    ) -> bool:
        if expression.endswith("pi"):
            prefix = expression[:-2]

            return prefix == "" or not prefix[-1].isalpha()

        if expression.endswith("e"):
            prefix = expression[:-1]

            return prefix == "" or not prefix[-1].isalpha()

        return False

    def expression_ends_with_operand(
        self,
        expression: str,
    ) -> bool:
        if expression == "":
            return False

        if expression[-1].isdigit() or expression[-1] == ".":
            return True

        if expression.endswith(")"):
            return True

        if self.expression_ends_with_constant(expression):
            return True

        return False

    def should_insert_multiplication(
        self,
        current: str,
        value: str,
    ) -> bool:
        if current == "":
            return False

        current_ends_operand = self.expression_ends_with_operand(current)

        new_is_number = value.isdigit()

        new_starts_operand = (
            value == "(" or self.is_constant(value) or self.is_function_prefix(value)
        )

        if current_ends_operand and new_starts_operand:
            return True

        if (
            current.endswith(")") or self.expression_ends_with_constant(current)
        ) and new_is_number:
            return True

        return False

    def current_number_segment(
        self,
        expression: str,
    ) -> str:
        separators = (
            "+",
            "-",
            "*",
            "/",
            "%",
            "(",
            ")",
        )

        last_separator_index = -1

        for index, character in enumerate(expression):
            if character in separators:
                last_separator_index = index

        return expression[last_separator_index + 1 :]

    def handle_decimal_point(
        self,
    ) -> None:
        current = self.display_var.get()

        if self.just_calculated:
            self.display_var.set("0.")
            self.previous_var.set("")
            self.just_calculated = False
            return

        if current.endswith(")") or self.expression_ends_with_constant(current):
            self.display_var.set(current + "*0.")
            return

        number_segment = self.current_number_segment(current)

        if "." in number_segment:
            return

        if current == "" or current.endswith(
            (
                "+",
                "-",
                "*",
                "/",
                "%",
                "//",
                "**",
                "(",
            )
        ):
            self.display_var.set(current + "0.")
            return

        self.display_var.set(current + ".")

    def unmatched_open_parentheses(
        self,
        expression: str,
    ) -> int:
        return max(
            0,
            expression.count("(") - expression.count(")"),
        )

    def can_close_parenthesis(
        self,
        expression: str,
    ) -> bool:
        if expression == "":
            return False

        if self.unmatched_open_parentheses(expression) == 0:
            return False

        invalid_endings = (
            "(",
            "+",
            "-",
            "*",
            "/",
            "%",
            "//",
            "**",
        )

        if expression.endswith(invalid_endings):
            return False

        return True

    def handle_closing_parenthesis(
        self,
    ) -> None:
        current = self.display_var.get()

        if not self.can_close_parenthesis(current):
            return

        self.display_var.set(current + ")")

        self.just_calculated = False

    def button_click(
        self,
        value: str,
    ) -> None:
        if value == ".":
            self.handle_decimal_point()
            return

        if value == ")":
            self.handle_closing_parenthesis()
            return

        current = self.display_var.get()

        if self.just_calculated:
            if self.is_operator(value):
                self.display_var.set(
                    append_to_display(
                        current,
                        value,
                    )
                )
            else:
                self.display_var.set(value)

            self.previous_var.set("")
            self.just_calculated = False
            return

        if self.is_operator(value):
            if current == "":
                if value == "-":
                    self.display_var.set("-")
                return

            if value == "-":
                if current.endswith(
                    (
                        "+",
                        "*",
                        "/",
                        "%",
                        "//",
                        "**",
                    )
                ):
                    self.display_var.set(current + "-")
                    return

            operator_suffixes = (
                "//",
                "**",
                "+",
                "-",
                "*",
                "/",
                "%",
            )

            for operator_value in operator_suffixes:
                if current.endswith(operator_value):
                    self.display_var.set(current[: -len(operator_value)] + value)
                    return

        if self.should_insert_multiplication(
            current,
            value,
        ):
            self.display_var.set(current + "*" + value)
            return

        self.display_var.set(
            append_to_display(
                current,
                value,
            )
        )

    def apply_to_current_expression(
        self,
        function_name: str,
    ) -> None:
        current = self.display_var.get().strip()

        if current == "":
            self.display_var.set(f"{function_name}(")
            self.just_calculated = False
            return

        self.display_var.set(f"{function_name}({current})")

        self.previous_var.set("")
        self.just_calculated = False

    def complete_parentheses(
        self,
        expression: str,
    ) -> str:
        missing_closing = self.unmatched_open_parentheses(expression)

        if missing_closing == 0:
            return expression

        return expression + ")" * missing_closing

    def clear_display(self) -> None:
        self.display_var.set("")
        self.previous_var.set("")
        self.just_calculated = False

    def backspace(self) -> None:
        current = self.display_var.get()

        self.display_var.set(backspace_display(current))

        self.just_calculated = False

    def get_angle_mode(
        self,
    ) -> AngleMode:
        mode = self.angle_mode_var.get()

        if mode == "degrees":
            return "degrees"

        return "radians"

    def update_mode_status(
        self,
    ) -> None:
        if self.angle_mode_var.get() == "degrees":
            self.mode_status_var.set("DEG")
        else:
            self.mode_status_var.set("RAD")

    def calculate(self) -> None:
        expression = self.display_var.get().strip()

        if expression == "":
            return

        expression = self.complete_parentheses(expression)

        try:
            result = calculate_expression(
                expression,
                self.get_angle_mode(),
            )

            formatted_result = format_number(result)

            self.previous_var.set(f"{expression} =")

            self.display_var.set(str(formatted_result))

            self.last_result = result
            self.just_calculated = True

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

        self.center_child_window(
            window,
            650,
            400,
        )

        window.minsize(
            500,
            300,
        )

        window.resizable(
            True,
            True,
        )

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

        window.transient(self.root)

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

    def save_last_result_to_memory(
        self,
    ) -> None:
        if self.last_result is None:
            messagebox.showinfo(
                "Memory",
                "There is no result to save.",
            )
            return

        result = self.last_result

        window = tk.Toplevel(self.root)
        window.title("Save to Memory")

        self.center_child_window(
            window,
            320,
            170,
        )

        window.resizable(
            False,
            False,
        )

        window.transient(self.root)

        window.grab_set()

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

        self.center_child_window(
            window,
            450,
            350,
        )

        window.minsize(
            400,
            300,
        )

        window.resizable(
            True,
            True,
        )

        window.transient(self.root)

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

    def get_keyboard_shortcuts_text(
        self,
    ) -> str:
        return (
            "GENERAL\n"
            "────────────────────────────────────\n"
            "Enter / Numpad Enter     Calculate\n"
            "Backspace                Delete last character\n"
            "Escape / Delete          Clear display\n"
            "Ctrl+A                   Clear display\n"
            "\n"
            "CALCULATOR\n"
            "────────────────────────────────────\n"
            "0-9                      Number input\n"
            "+ - * / %                Operators\n"
            "**                       Power\n"
            "//                       Floor division\n"
            "( )                      Parentheses\n"
            ".                        Decimal point\n"
            "\n"
            "SCIENTIFIC\n"
            "────────────────────────────────────\n"
            "Ctrl+P                   π\n"
            "Ctrl+E                   e\n"
            "Ctrl+R                   Square root\n"
            "Ctrl+Q                   Square\n"
            "Ctrl+I                   Reciprocal\n"
            "Ctrl+F                   Factorial\n"
            "Ctrl+G                   Base-10 logarithm\n"
            "Ctrl+N                   Natural logarithm\n"
            "\n"
            "TRIGONOMETRY\n"
            "────────────────────────────────────\n"
            "Ctrl+1                   sin\n"
            "Ctrl+2                   cos\n"
            "Ctrl+3                   tan\n"
            "Ctrl+4                   asin\n"
            "Ctrl+5                   acos\n"
            "Ctrl+6                   atan\n"
            "\n"
            "ANGLE MODE\n"
            "────────────────────────────────────\n"
            "Ctrl+D                   Degrees\n"
            "Ctrl+T                   Radians\n"
            "\n"
            "OTHER\n"
            "────────────────────────────────────\n"
            "Ctrl+Space               ANS\n"
            "Ctrl+H                   History\n"
            "Ctrl+M                   Memory\n"
            "Ctrl+S                   Save result to memory\n"
            "Ctrl+L                   Clear display\n"
            "F1                       Keyboard shortcuts"
        )

    def show_keyboard_shortcuts(
        self,
    ) -> None:
        window = tk.Toplevel(self.root)

        window.title("Keyboard Shortcuts")

        self.center_child_window(
            window,
            520,
            620,
        )

        window.minsize(
            460,
            500,
        )

        window.resizable(
            True,
            True,
        )

        window.transient(self.root)

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
            text="Keyboard Shortcuts",
            font=(
                "Segoe UI",
                16,
                "bold",
            ),
        ).pack(
            pady=(0, 12),
        )

        text_frame = ttk.Frame(frame)
        text_frame.pack(
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
        )
        scrollbar.pack(
            side="right",
            fill="y",
        )

        text_box = tk.Text(
            text_frame,
            font=(
                "Consolas",
                10,
            ),
            wrap="none",
            yscrollcommand=scrollbar.set,
        )
        text_box.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.config(command=text_box.yview)

        text_box.insert(
            "1.0",
            self.get_keyboard_shortcuts_text(),
        )

        text_box.config(
            state="disabled",
        )

        ttk.Button(
            frame,
            text="Close",
            command=window.destroy,
        ).pack(
            pady=(12, 0),
        )

        window.focus_set()
        window.lift()

    def show_about(self) -> None:
        messagebox.showinfo(
            "About",
            (
                f"Simple Scientific Calculator "
                f"{__version__}\n\n"
                "Built with Python, tkinter, ttk, "
                "JSON, AST, and pytest.\n\n"
                "Scientific functions include:\n"
                "- Trigonometry\n"
                "- Inverse trigonometry\n"
                "- Logarithms\n"
                "- Factorials\n"
                "- Powers and reciprocals\n"
                "- Mathematical constants\n"
                "- Degree/radian modes\n"
                "- Automatic parenthesis completion\n"
                "- Smart operator handling\n"
                "- Decimal input protection\n"
                "- Implicit multiplication\n"
                "- Smart closing-parenthesis handling\n"
                "- Smart constant and operand detection\n"
                "- Validated keyboard input\n"
                "- Scientific keyboard shortcuts\n"
                "- Built-in shortcut reference\n"
                "- Styled desktop interface\n"
                "- Active angle-mode status\n"
                "- Centered and resizable windows\n\n"
                "Also includes history, memory, "
                "persistent storage, and keyboard shortcuts."
            ),
        )

    def create_keyboard_shortcuts(
        self,
    ) -> None:
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
        self.root.bind(
            "<Control-a>",
            self.clear_shortcut,
        )

        self.root.bind(
            "<Control-p>",
            self.pi_shortcut,
        )
        self.root.bind(
            "<Control-e>",
            self.e_shortcut,
        )
        self.root.bind(
            "<Control-r>",
            self.sqrt_shortcut,
        )
        self.root.bind(
            "<Control-q>",
            self.square_shortcut,
        )
        self.root.bind(
            "<Control-i>",
            self.reciprocal_shortcut,
        )
        self.root.bind(
            "<Control-f>",
            self.factorial_shortcut,
        )
        self.root.bind(
            "<Control-g>",
            self.log_shortcut,
        )
        self.root.bind(
            "<Control-n>",
            self.ln_shortcut,
        )

        self.root.bind(
            "<Control-Key-1>",
            self.sin_shortcut,
        )
        self.root.bind(
            "<Control-Key-2>",
            self.cos_shortcut,
        )
        self.root.bind(
            "<Control-Key-3>",
            self.tan_shortcut,
        )
        self.root.bind(
            "<Control-Key-4>",
            self.asin_shortcut,
        )
        self.root.bind(
            "<Control-Key-5>",
            self.acos_shortcut,
        )
        self.root.bind(
            "<Control-Key-6>",
            self.atan_shortcut,
        )

        self.root.bind(
            "<Control-d>",
            self.degree_mode_shortcut,
        )
        self.root.bind(
            "<Control-t>",
            self.radian_mode_shortcut,
        )
        self.root.bind(
            "<Control-space>",
            self.ans_shortcut,
        )

        self.root.bind(
            "<F1>",
            self.keyboard_shortcuts_shortcut,
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

    def pi_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("pi")
        return "break"

    def e_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("e")
        return "break"

    def sqrt_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("sqrt")
        return "break"

    def square_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("square")
        return "break"

    def reciprocal_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("reciprocal")
        return "break"

    def factorial_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("factorial")
        return "break"

    def log_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("log")
        return "break"

    def ln_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.apply_to_current_expression("ln")
        return "break"

    def sin_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("sin(")
        return "break"

    def cos_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("cos(")
        return "break"

    def tan_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("tan(")
        return "break"

    def asin_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("asin(")
        return "break"

    def acos_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("acos(")
        return "break"

    def atan_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.button_click("atan(")
        return "break"

    def degree_mode_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.angle_mode_var.set("degrees")
        self.update_mode_status()
        return "break"

    def radian_mode_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.angle_mode_var.set("radians")
        self.update_mode_status()
        return "break"

    def ans_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.use_last_result()
        return "break"

    def keyboard_shortcuts_shortcut(
        self,
        event: tk.Event,
    ) -> str:
        self.show_keyboard_shortcuts()
        return "break"

    def handle_keyboard_character(
        self,
        char: str,
    ) -> None:
        current = self.display_var.get()

        if char == "*":
            if current.endswith("*"):
                self.button_click("**")
                return

            self.button_click("*")
            return

        if char == "/":
            if current.endswith("/"):
                self.button_click("//")
                return

            self.button_click("/")
            return

        self.button_click(char)

    def key_pressed(
        self,
        event: tk.Event,
    ) -> str | None:
        key = event.keysym
        char = event.char

        if char and char in "0123456789.+-*/%()":
            self.handle_keyboard_character(char)
            return "break"

        if key in {
            "Return",
            "KP_Enter",
        }:
            self.calculate()
            return "break"

        if key == "BackSpace":
            self.backspace()
            return "break"

        if key in {
            "Escape",
            "Delete",
        }:
            self.clear_display()
            return "break"

        return None

    def close_program(self) -> None:
        self.save()
        self.root.destroy()
