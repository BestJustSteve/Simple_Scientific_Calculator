from unittest.mock import patch

from calculator.gui import CalculatorApp


class FakeStringVar:
    def __init__(
        self,
        value: str = "",
    ) -> None:
        self.value = value

    def get(self) -> str:
        return self.value

    def set(
        self,
        value: str,
    ) -> None:
        self.value = value


def create_app() -> CalculatorApp:
    app = CalculatorApp.__new__(CalculatorApp)

    app.display_var = FakeStringVar()
    app.previous_var = FakeStringVar()
    app.angle_mode_var = FakeStringVar("radians")
    app.mode_status_var = FakeStringVar("RAD")

    app.history = []
    app.memory = {}
    app.last_result = None
    app.just_calculated = False

    return app


def test_keyboard_shortcuts_text_contains_general_section():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "GENERAL" in text
    assert "Enter / Numpad Enter" in text
    assert "Backspace" in text
    assert "Escape / Delete" in text


def test_keyboard_shortcuts_text_contains_calculator_section():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "CALCULATOR" in text
    assert "**" in text
    assert "//" in text
    assert "Decimal point" in text


def test_keyboard_shortcuts_text_contains_scientific_section():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "SCIENTIFIC" in text
    assert "Ctrl+P" in text
    assert "Ctrl+R" in text
    assert "Ctrl+Q" in text
    assert "Ctrl+F" in text
    assert "Ctrl+G" in text
    assert "Ctrl+N" in text


def test_keyboard_shortcuts_text_contains_trigonometry():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "TRIGONOMETRY" in text
    assert "Ctrl+1" in text
    assert "Ctrl+2" in text
    assert "Ctrl+3" in text
    assert "Ctrl+4" in text
    assert "Ctrl+5" in text
    assert "Ctrl+6" in text


def test_keyboard_shortcuts_text_contains_angle_modes():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "ANGLE MODE" in text
    assert "Ctrl+D" in text
    assert "Degrees" in text
    assert "Ctrl+T" in text
    assert "Radians" in text


def test_keyboard_shortcuts_text_contains_other_shortcuts():
    app = create_app()

    text = app.get_keyboard_shortcuts_text()

    assert "OTHER" in text
    assert "Ctrl+Space" in text
    assert "Ctrl+H" in text
    assert "Ctrl+M" in text
    assert "Ctrl+S" in text
    assert "Ctrl+L" in text
    assert "F1" in text


def test_keyboard_shortcuts_shortcut_opens_window():
    app = create_app()

    with patch.object(
        app,
        "show_keyboard_shortcuts",
    ) as mock_show:
        result = app.keyboard_shortcuts_shortcut(None)

    mock_show.assert_called_once_with()
    assert result == "break"


def test_pi_shortcut_still_works():
    app = create_app()

    result = app.pi_shortcut(None)

    assert app.display_var.get() == "pi"
    assert result == "break"


def test_sqrt_shortcut_still_works():
    app = create_app()

    app.display_var.set("144")

    result = app.sqrt_shortcut(None)

    assert app.display_var.get() == "sqrt(144)"

    assert result == "break"


def test_degree_shortcut_still_works():
    app = create_app()

    app.angle_mode_var.set("radians")

    result = app.degree_mode_shortcut(None)

    assert app.angle_mode_var.get() == "degrees"

    assert result == "break"


def test_radian_shortcut_still_works():
    app = create_app()

    app.angle_mode_var.set("degrees")

    result = app.radian_mode_shortcut(None)

    assert app.angle_mode_var.get() == "radians"

    assert result == "break"


def test_ans_shortcut_still_works():
    app = create_app()

    app.last_result = 42

    result = app.ans_shortcut(None)

    assert app.display_var.get() == "42"
    assert result == "break"
