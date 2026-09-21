from unittest.mock import MagicMock, patch

import pytest

from calculator.gui import CalculatorApp


class FakeEvent:
    def __init__(
        self,
        char: str = "",
        keysym: str = "",
    ) -> None:
        self.char = char
        self.keysym = keysym


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


def test_button_click():
    app = create_app()

    app.display_var.set("12")
    app.button_click("3")

    assert app.display_var.get() == "123"


def test_clear_display():
    app = create_app()

    app.display_var.set("123")
    app.previous_var.set("1 + 2 =")
    app.just_calculated = True

    app.clear_display()

    assert app.display_var.get() == ""
    assert app.previous_var.get() == ""
    assert app.just_calculated is False


def test_backspace():
    app = create_app()

    app.display_var.set("123")
    app.just_calculated = True

    app.backspace()

    assert app.display_var.get() == "12"
    assert app.just_calculated is False


def test_backspace_empty_display():
    app = create_app()

    app.backspace()

    assert app.display_var.get() == ""


def test_default_angle_mode_is_radians():
    app = create_app()

    assert app.get_angle_mode() == "radians"


def test_degree_angle_mode():
    app = create_app()

    app.angle_mode_var.set("degrees")

    assert app.get_angle_mode() == "degrees"


def test_invalid_angle_mode_falls_back_to_radians():
    app = create_app()

    app.angle_mode_var.set("invalid")

    assert app.get_angle_mode() == "radians"


def test_calculate_addition():
    app = create_app()

    app.display_var.set("2 + 3")

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.calculate()

    assert app.display_var.get() == "5"
    assert app.previous_var.get() == "2 + 3 ="
    assert app.last_result == 5
    assert app.just_calculated is True
    assert len(app.history) == 1
    assert app.history[0]["expression"] == "2 + 3"
    assert app.history[0]["result"] == 5

    mock_save.assert_called_once()


def test_calculate_operator_precedence():
    app = create_app()

    app.display_var.set("2 + 3 * 4")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "14"


def test_calculate_decimal():
    app = create_app()

    app.display_var.set("5 / 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "2.5"


def test_calculate_sine_in_degrees():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("sin(90)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(1)


def test_calculate_cosine_in_degrees():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("cos(180)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "-1"


def test_calculate_cosine_90_degrees_formats_zero():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("cos(90)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "0"


def test_calculate_tangent_in_degrees():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("tan(45)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"


def test_calculate_sine_in_radians():
    app = create_app()

    app.display_var.set("sin(pi / 2)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"


def test_calculate_square_root():
    app = create_app()

    app.display_var.set("sqrt(144)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"


def test_insert_sine_function():
    app = create_app()

    app.button_click("sin(")

    assert app.display_var.get() == "sin("


def test_insert_inverse_sine():
    app = create_app()

    app.button_click("asin(")

    assert app.display_var.get() == "asin("


def test_insert_pi_constant():
    app = create_app()

    app.button_click("pi")

    assert app.display_var.get() == "pi"


def test_insert_e_constant():
    app = create_app()

    app.button_click("e")

    assert app.display_var.get() == "e"


def test_apply_square_to_current_expression():
    app = create_app()

    app.display_var.set("12")

    app.apply_to_current_expression("square")

    assert app.display_var.get() == "square(12)"


def test_apply_reciprocal():
    app = create_app()

    app.display_var.set("4")

    app.apply_to_current_expression("reciprocal")

    assert app.display_var.get() == "reciprocal(4)"


def test_apply_factorial():
    app = create_app()

    app.display_var.set("5")

    app.apply_to_current_expression("factorial")

    assert app.display_var.get() == "factorial(5)"


def test_apply_square_root():
    app = create_app()

    app.display_var.set("144")

    app.apply_to_current_expression("sqrt")

    assert app.display_var.get() == "sqrt(144)"


def test_apply_log():
    app = create_app()

    app.display_var.set("1000")

    app.apply_to_current_expression("log")

    assert app.display_var.get() == "log(1000)"


def test_apply_ln():
    app = create_app()

    app.display_var.set("e")

    app.apply_to_current_expression("ln")

    assert app.display_var.get() == "ln(e)"


def test_apply_power_of_ten():
    app = create_app()

    app.display_var.set("3")

    app.apply_to_current_expression("pow10")

    assert app.display_var.get() == "pow10(3)"


def test_apply_exponential():
    app = create_app()

    app.display_var.set("1")

    app.apply_to_current_expression("exp")

    assert app.display_var.get() == "exp(1)"


def test_apply_function_to_empty_display():
    app = create_app()

    app.apply_to_current_expression("sqrt")

    assert app.display_var.get() == "sqrt("


def test_number_starts_new_expression_after_calculation():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("7")

    assert app.display_var.get() == "7"
    assert app.just_calculated is False


def test_operator_continues_after_calculation():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("+")

    assert app.display_var.get() == "4+"


def test_continue_calculation_from_result():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("+")
    app.button_click("6")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "10"


def test_scientific_operation_uses_previous_result():
    app = create_app()

    app.display_var.set("12")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.apply_to_current_expression("square")

    assert app.display_var.get() == "square(12)"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "144"


def test_complete_one_missing_parenthesis():
    app = create_app()

    result = app.complete_parentheses("sin(90")

    assert result == "sin(90)"


def test_complete_multiple_missing_parentheses():
    app = create_app()

    result = app.complete_parentheses("sqrt(square(12")

    assert result == "sqrt(square(12))"


def test_complete_expression_unchanged():
    app = create_app()

    result = app.complete_parentheses("sin(90)")

    assert result == "sin(90)"


def test_auto_close_sine():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("sin(90")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"
    assert app.previous_var.get() == "sin(90) ="


def test_auto_close_nested_functions():
    app = create_app()

    app.display_var.set("sqrt(square(12")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"


def test_is_operator():
    app = create_app()

    assert app.is_operator("+")
    assert app.is_operator("-")
    assert app.is_operator("*")
    assert app.is_operator("/")
    assert app.is_operator("%")
    assert app.is_operator("//")
    assert app.is_operator("**")
    assert not app.is_operator("5")


def test_operator_replaces_previous_operator():
    app = create_app()

    app.display_var.set("5+")
    app.button_click("*")

    assert app.display_var.get() == "5*"


def test_power_replaces_previous_operator():
    app = create_app()

    app.display_var.set("5+")
    app.button_click("**")

    assert app.display_var.get() == "5**"


def test_operator_replaces_power_operator():
    app = create_app()

    app.display_var.set("5**")
    app.button_click("/")

    assert app.display_var.get() == "5/"


def test_minus_can_start_expression():
    app = create_app()

    app.button_click("-")

    assert app.display_var.get() == "-"


def test_plus_cannot_start_expression():
    app = create_app()

    app.button_click("+")

    assert app.display_var.get() == ""


def test_minus_after_multiplication():
    app = create_app()

    app.display_var.set("5*")
    app.button_click("-")

    assert app.display_var.get() == "5*-"


def test_negative_number_expression_calculates():
    app = create_app()

    app.button_click("5")
    app.button_click("*")
    app.button_click("-")
    app.button_click("2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "-10"


def test_current_number_segment():
    app = create_app()

    assert app.current_number_segment("5+12.5") == "12.5"


def test_current_number_segment_function():
    app = create_app()

    assert app.current_number_segment("sin(0.5") == "0.5"


def test_decimal_at_start():
    app = create_app()

    app.button_click(".")

    assert app.display_var.get() == "0."


def test_decimal_after_operator():
    app = create_app()

    app.button_click("5")
    app.button_click("+")
    app.button_click(".")

    assert app.display_var.get() == "5+0."


def test_second_decimal_ignored():
    app = create_app()

    app.button_click("1")
    app.button_click(".")
    app.button_click("2")
    app.button_click(".")
    app.button_click("3")

    assert app.display_var.get() == "1.23"


def test_decimal_inside_function():
    app = create_app()

    app.button_click("sin(")
    app.button_click(".")
    app.button_click("5")

    assert app.display_var.get() == "sin(0.5"


def test_decimal_after_result_starts_new_number():
    app = create_app()

    app.display_var.set("2+2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click(".")

    assert app.display_var.get() == "0."


def test_decimal_after_closing_parenthesis_uses_multiplication():
    app = create_app()

    app.display_var.set("(2)")
    app.button_click(".")

    assert app.display_var.get() == "(2)*0."


def test_decimal_after_pi_uses_multiplication():
    app = create_app()

    app.display_var.set("pi")
    app.button_click(".")

    assert app.display_var.get() == "pi*0."


def test_is_constant():
    app = create_app()

    assert app.is_constant("pi")
    assert app.is_constant("e")
    assert not app.is_constant("sin(")
    assert not app.is_constant("5")


def test_is_function_prefix():
    app = create_app()

    assert app.is_function_prefix("sin(")
    assert app.is_function_prefix("cos(")
    assert app.is_function_prefix("tan(")
    assert app.is_function_prefix("asin(")
    assert app.is_function_prefix("acos(")
    assert app.is_function_prefix("atan(")
    assert not app.is_function_prefix("pi")


def test_expression_ends_with_pi():
    app = create_app()

    assert app.expression_ends_with_constant("2*pi")


def test_expression_ends_with_e():
    app = create_app()

    assert app.expression_ends_with_constant("2*e")


def test_expression_does_not_end_constant():
    app = create_app()

    assert not app.expression_ends_with_constant("2+3")


def test_number_followed_by_pi_inserts_multiplication():
    app = create_app()

    app.button_click("2")
    app.button_click("pi")

    assert app.display_var.get() == "2*pi"


def test_number_followed_by_e_inserts_multiplication():
    app = create_app()

    app.button_click("2")
    app.button_click("e")

    assert app.display_var.get() == "2*e"


def test_number_followed_by_parenthesis_inserts_multiplication():
    app = create_app()

    app.button_click("2")
    app.button_click("(")

    assert app.display_var.get() == "2*("


def test_number_followed_by_function_inserts_multiplication():
    app = create_app()

    app.button_click("3")
    app.button_click("sin(")

    assert app.display_var.get() == "3*sin("


def test_closing_parenthesis_followed_by_number_inserts_multiplication():
    app = create_app()

    app.display_var.set("(2)")
    app.button_click("3")

    assert app.display_var.get() == "(2)*3"


def test_closing_parenthesis_followed_by_parenthesis():
    app = create_app()

    app.display_var.set("(2)")
    app.button_click("(")

    assert app.display_var.get() == "(2)*("


def test_closing_parenthesis_followed_by_pi():
    app = create_app()

    app.display_var.set("(2)")
    app.button_click("pi")

    assert app.display_var.get() == "(2)*pi"


def test_closing_parenthesis_followed_by_function():
    app = create_app()

    app.display_var.set("(2)")
    app.button_click("sin(")

    assert app.display_var.get() == "(2)*sin("


def test_pi_followed_by_number():
    app = create_app()

    app.button_click("pi")
    app.button_click("2")

    assert app.display_var.get() == "pi*2"


def test_pi_followed_by_parenthesis():
    app = create_app()

    app.button_click("pi")
    app.button_click("(")

    assert app.display_var.get() == "pi*("


def test_pi_followed_by_e():
    app = create_app()

    app.button_click("pi")
    app.button_click("e")

    assert app.display_var.get() == "pi*e"


def test_pi_followed_by_function():
    app = create_app()

    app.button_click("pi")
    app.button_click("sin(")

    assert app.display_var.get() == "pi*sin("


def test_regular_multi_digit_number_does_not_insert_multiplication():
    app = create_app()

    app.button_click("1")
    app.button_click("2")
    app.button_click("3")

    assert app.display_var.get() == "123"


def test_implicit_pi_multiplication_calculates():
    app = create_app()

    app.button_click("2")
    app.button_click("pi")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(2 * 3.141592653589793)


def test_implicit_parenthesis_multiplication_calculates():
    app = create_app()

    app.button_click("2")
    app.button_click("(")
    app.button_click("3")
    app.button_click("+")
    app.button_click("4")

    assert app.display_var.get() == "2*(3+4"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "14"


def test_two_parenthesized_expressions_multiply():
    app = create_app()

    app.button_click("(")
    app.button_click("2")
    app.button_click(")")
    app.button_click("(")
    app.button_click("3")
    app.button_click(")")

    assert app.display_var.get() == "(2)*(3)"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "6"


def test_implicit_function_multiplication_calculates():
    app = create_app()

    app.angle_mode_var.set("degrees")

    app.button_click("3")
    app.button_click("sin(")
    app.button_click("30")

    assert app.display_var.get() == "3*sin(30"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(1.5)


def test_implicit_e_multiplication_calculates():
    app = create_app()

    app.button_click("2")
    app.button_click("e")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(2 * 2.718281828459045)


def test_calculate_empty_expression():
    app = create_app()

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.calculate()

    mock_save.assert_not_called()


def test_calculate_division_by_zero():
    app = create_app()

    app.display_var.set("10 / 0")

    with (
        patch("calculator.gui.messagebox.showerror") as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "Cannot divide by zero.",
    )
    mock_save.assert_not_called()


def test_calculate_invalid_expression():
    app = create_app()

    app.display_var.set("2 +")

    with (
        patch("calculator.gui.messagebox.showerror") as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "Invalid calculation.",
    )
    mock_save.assert_not_called()


def test_calculate_overflow():
    app = create_app()

    app.display_var.set("10 ** 1000000")

    with (
        patch(
            "calculator.gui.calculate_expression",
            side_effect=OverflowError,
        ),
        patch("calculator.gui.messagebox.showerror") as mock_error,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "That number is too large.",
    )


def test_use_last_result():
    app = create_app()

    app.last_result = 42
    app.use_last_result()

    assert app.display_var.get() == "42"


def test_use_last_result_none():
    app = create_app()

    with patch("calculator.gui.messagebox.showinfo") as mock_info:
        app.use_last_result()

    mock_info.assert_called_once()


def test_load_saved_data():
    app = create_app()

    fake_history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    fake_memory = {
        "answer": 4,
    }

    with patch(
        "calculator.gui.load_data",
        return_value=(
            fake_history,
            fake_memory,
            4,
        ),
    ):
        app.load_saved_data()

    assert app.history == fake_history
    assert app.memory == fake_memory
    assert app.last_result == 4


def test_save():
    app = create_app()

    app.memory = {
        "answer": 4,
    }
    app.last_result = 4

    app.settings = {
        "angle_mode": "radians",
        "geometry": "",
    }

    with patch("calculator.gui.save_data") as mock_save:
        app.save()

    mock_save.assert_called_once_with(
        app.history,
        app.memory,
        app.last_result,
        app.settings,
    )


def test_save_oserror():
    app = create_app()

    with (
        patch(
            "calculator.gui.save_data",
            side_effect=OSError,
        ),
        patch("calculator.gui.messagebox.showerror") as mock_error,
    ):
        app.save()

    mock_error.assert_called_once_with(
        "Error",
        "Calculator data could not be saved.",
    )


def test_use_memory_value():
    app = create_app()

    mock_window = MagicMock()

    app.use_memory_value(
        25,
        mock_window,
    )

    assert app.display_var.get() == "25"

    mock_window.destroy.assert_called_once()


def test_delete_memory_value():
    app = create_app()

    app.memory = {
        "tax": 0.08,
    }

    mock_window = MagicMock()

    with (
        patch.object(
            app,
            "save",
        ) as mock_save,
        patch.object(
            app,
            "show_memory",
        ) as mock_show_memory,
    ):
        app.delete_memory_value(
            "tax",
            mock_window,
        )

    assert "tax" not in app.memory

    mock_save.assert_called_once()
    mock_window.destroy.assert_called_once()
    mock_show_memory.assert_called_once()


def test_delete_missing_memory_value():
    app = create_app()

    mock_window = MagicMock()

    with (
        patch.object(
            app,
            "save",
        ) as mock_save,
        patch.object(
            app,
            "show_memory",
        ) as mock_show_memory,
    ):
        app.delete_memory_value(
            "missing",
            mock_window,
        )

    mock_save.assert_not_called()
    mock_window.destroy.assert_not_called()
    mock_show_memory.assert_not_called()


def test_show_history_shortcut():
    app = create_app()

    with patch.object(
        app,
        "show_history",
    ) as mock_method:
        app.show_history_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_show_memory_shortcut():
    app = create_app()

    with patch.object(
        app,
        "show_memory",
    ) as mock_method:
        app.show_memory_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_save_memory_shortcut():
    app = create_app()

    with patch.object(
        app,
        "save_last_result_to_memory",
    ) as mock_method:
        app.save_memory_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_clear_shortcut():
    app = create_app()

    with patch.object(
        app,
        "clear_display",
    ) as mock_method:
        app.clear_shortcut(
            None,
        )

    mock_method.assert_called_once()


def test_unmatched_open_parentheses_none():
    app = create_app()

    result = app.unmatched_open_parentheses("2+2")

    assert result == 0


def test_unmatched_open_parentheses_one():
    app = create_app()

    result = app.unmatched_open_parentheses("(2+2")

    assert result == 1


def test_unmatched_open_parentheses_nested():
    app = create_app()

    result = app.unmatched_open_parentheses("sqrt((2+2")

    assert result == 2


def test_unmatched_open_parentheses_complete():
    app = create_app()

    result = app.unmatched_open_parentheses("sqrt((2+2))")

    assert result == 0


def test_cannot_close_parenthesis_on_empty_expression():
    app = create_app()

    assert app.can_close_parenthesis("") is False


def test_cannot_close_without_open_parenthesis():
    app = create_app()

    assert app.can_close_parenthesis("2+2") is False


def test_can_close_valid_parenthesis():
    app = create_app()

    assert app.can_close_parenthesis("(2+2") is True


def test_cannot_close_immediately_after_open_parenthesis():
    app = create_app()

    assert app.can_close_parenthesis("(") is False


def test_cannot_close_after_operator():
    app = create_app()

    assert app.can_close_parenthesis("(2+") is False


def test_cannot_close_after_multiplication():
    app = create_app()

    assert app.can_close_parenthesis("(2*") is False


def test_cannot_close_after_power_operator():
    app = create_app()

    assert app.can_close_parenthesis("(2**") is False


def test_closing_parenthesis_is_added_when_valid():
    app = create_app()

    app.display_var.set("(2+3")

    app.button_click(")")

    assert app.display_var.get() == "(2+3)"


def test_extra_closing_parenthesis_is_ignored():
    app = create_app()

    app.display_var.set("(2+3)")

    app.button_click(")")

    assert app.display_var.get() == "(2+3)"


def test_empty_parentheses_are_prevented():
    app = create_app()

    app.button_click("(")
    app.button_click(")")

    assert app.display_var.get() == "("


def test_empty_function_parentheses_are_prevented():
    app = create_app()

    app.button_click("sin(")
    app.button_click(")")

    assert app.display_var.get() == "sin("


def test_closing_parenthesis_after_number_in_function():
    app = create_app()

    app.button_click("sin(")
    app.button_click("30")
    app.button_click(")")

    assert app.display_var.get() == "sin(30)"


def test_closing_parenthesis_after_constant():
    app = create_app()

    app.button_click("(")
    app.button_click("pi")
    app.button_click(")")

    assert app.display_var.get() == "(pi)"


def test_closing_parenthesis_after_decimal():
    app = create_app()

    app.button_click("(")
    app.button_click("2")
    app.button_click(".")
    app.button_click("5")
    app.button_click(")")

    assert app.display_var.get() == "(2.5)"


def test_nested_parentheses_close_one_at_a_time():
    app = create_app()

    app.button_click("(")
    app.button_click("(")
    app.button_click("2")
    app.button_click("+")
    app.button_click("3")

    app.button_click(")")

    assert app.display_var.get() == "((2+3)"

    app.button_click(")")

    assert app.display_var.get() == "((2+3))"

    app.button_click(")")

    assert app.display_var.get() == "((2+3))"


def test_invalid_close_after_operator_is_ignored():
    app = create_app()

    app.button_click("(")
    app.button_click("2")
    app.button_click("+")
    app.button_click(")")

    assert app.display_var.get() == "(2+"


def test_parenthesized_expression_calculates():
    app = create_app()

    app.button_click("(")
    app.button_click("2")
    app.button_click("+")
    app.button_click("3")
    app.button_click(")")
    app.button_click("*")
    app.button_click("4")

    assert app.display_var.get() == "(2+3)*4"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "20"


def test_constant_detection_does_not_confuse_word_ending_in_e():
    app = create_app()

    assert app.expression_ends_with_constant("square") is False


def test_constant_detection_pi():
    app = create_app()

    assert app.expression_ends_with_constant("2*pi") is True


def test_constant_detection_e():
    app = create_app()

    assert app.expression_ends_with_constant("2*e") is True


def test_expression_ends_with_number_operand():
    app = create_app()

    assert app.expression_ends_with_operand("123") is True


def test_expression_ends_with_parenthesis_operand():
    app = create_app()

    assert app.expression_ends_with_operand("sin(30)") is True


def test_expression_ends_with_pi_operand():
    app = create_app()

    assert app.expression_ends_with_operand("pi") is True


def test_expression_ends_with_e_operand():
    app = create_app()

    assert app.expression_ends_with_operand("e") is True


def test_operator_is_not_operand():
    app = create_app()

    assert app.expression_ends_with_operand("2+") is False


def test_pi_followed_by_e_inserts_multiplication():
    app = create_app()

    app.button_click("pi")
    app.button_click("e")

    assert app.display_var.get() == "pi*e"


def test_e_followed_by_pi_inserts_multiplication():
    app = create_app()

    app.button_click("e")
    app.button_click("pi")

    assert app.display_var.get() == "e*pi"


def test_e_followed_by_e_inserts_multiplication():
    app = create_app()

    app.button_click("e")
    app.button_click("e")

    assert app.display_var.get() == "e*e"


def test_closed_function_followed_by_number():
    app = create_app()

    app.button_click("sin(")
    app.button_click("30")
    app.button_click(")")
    app.button_click("2")

    assert app.display_var.get() == "sin(30)*2"


def test_closed_function_followed_by_pi():
    app = create_app()

    app.button_click("sin(")
    app.button_click("30")
    app.button_click(")")
    app.button_click("pi")

    assert app.display_var.get() == "sin(30)*pi"


def test_closed_function_followed_by_function():
    app = create_app()

    app.button_click("sin(")
    app.button_click("30")
    app.button_click(")")
    app.button_click("cos(")

    assert app.display_var.get() == "sin(30)*cos("


def test_function_can_be_nested_inside_open_function():
    app = create_app()

    app.button_click("sin(")
    app.button_click("cos(")

    assert app.display_var.get() == "sin(cos("


def test_constant_multiplication_calculates():
    app = create_app()

    app.button_click("pi")
    app.button_click("e")

    assert app.display_var.get() == "pi*e"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(
        3.141592653589793 * 2.718281828459045
    )


def test_closed_function_times_number_calculates():
    app = create_app()

    app.angle_mode_var.set("degrees")

    app.button_click("sin(")
    app.button_click("30")
    app.button_click(")")
    app.button_click("2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(app.display_var.get()) == pytest.approx(1)


def test_keyboard_digit():
    app = create_app()

    event = FakeEvent(
        char="5",
        keysym="5",
    )

    result = app.key_pressed(event)

    assert app.display_var.get() == "5"
    assert result == "break"


def test_keyboard_builds_number():
    app = create_app()

    for character in "123":
        app.key_pressed(
            FakeEvent(
                char=character,
                keysym=character,
            )
        )

    assert app.display_var.get() == "123"


def test_keyboard_decimal_uses_decimal_protection():
    app = create_app()

    for character in "1.2.3":
        app.key_pressed(
            FakeEvent(
                char=character,
                keysym=character,
            )
        )

    assert app.display_var.get() == "1.23"


def test_keyboard_leading_decimal_becomes_zero_decimal():
    app = create_app()

    app.key_pressed(
        FakeEvent(
            char=".",
            keysym="period",
        )
    )

    assert app.display_var.get() == "0."


def test_keyboard_operator_replacement():
    app = create_app()

    for character in "5+":
        app.key_pressed(
            FakeEvent(
                char=character,
                keysym=character,
            )
        )

    app.key_pressed(
        FakeEvent(
            char="*",
            keysym="asterisk",
        )
    )

    assert app.display_var.get() == "5*"


def test_keyboard_double_asterisk_creates_power():
    app = create_app()

    app.key_pressed(
        FakeEvent(
            char="2",
            keysym="2",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="*",
            keysym="asterisk",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="*",
            keysym="asterisk",
        )
    )

    assert app.display_var.get() == "2**"


def test_keyboard_double_slash_creates_floor_division():
    app = create_app()

    app.key_pressed(
        FakeEvent(
            char="1",
            keysym="1",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="0",
            keysym="0",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="/",
            keysym="slash",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="/",
            keysym="slash",
        )
    )

    assert app.display_var.get() == "10//"


def test_keyboard_parentheses_use_validation():
    app = create_app()

    app.key_pressed(
        FakeEvent(
            char="(",
            keysym="parenleft",
        )
    )
    app.key_pressed(
        FakeEvent(
            char="2",
            keysym="2",
        )
    )
    app.key_pressed(
        FakeEvent(
            char=")",
            keysym="parenright",
        )
    )
    app.key_pressed(
        FakeEvent(
            char=")",
            keysym="parenright",
        )
    )

    assert app.display_var.get() == "(2)"


def test_keyboard_invalid_closing_parenthesis_is_ignored():
    app = create_app()

    app.key_pressed(
        FakeEvent(
            char=")",
            keysym="parenright",
        )
    )

    assert app.display_var.get() == ""


def test_keyboard_negative_number():
    app = create_app()

    for character in "-5":
        app.key_pressed(
            FakeEvent(
                char=character,
                keysym=character,
            )
        )

    assert app.display_var.get() == "-5"


def test_keyboard_enter_calculates():
    app = create_app()

    app.display_var.set("2+2")

    with patch.object(
        app,
        "save",
    ):
        result = app.key_pressed(
            FakeEvent(
                keysym="Return",
            )
        )

    assert app.display_var.get() == "4"
    assert result == "break"


def test_keyboard_numpad_enter_calculates():
    app = create_app()

    app.display_var.set("3*4")

    with patch.object(
        app,
        "save",
    ):
        result = app.key_pressed(
            FakeEvent(
                keysym="KP_Enter",
            )
        )

    assert app.display_var.get() == "12"
    assert result == "break"


def test_keyboard_backspace():
    app = create_app()

    app.display_var.set("123")

    result = app.key_pressed(
        FakeEvent(
            keysym="BackSpace",
        )
    )

    assert app.display_var.get() == "12"
    assert result == "break"


def test_keyboard_escape_clears():
    app = create_app()

    app.display_var.set("123")

    result = app.key_pressed(
        FakeEvent(
            keysym="Escape",
        )
    )

    assert app.display_var.get() == ""
    assert result == "break"


def test_keyboard_delete_clears():
    app = create_app()

    app.display_var.set("123")

    result = app.key_pressed(
        FakeEvent(
            keysym="Delete",
        )
    )

    assert app.display_var.get() == ""
    assert result == "break"


def test_keyboard_unknown_key_is_ignored():
    app = create_app()

    result = app.key_pressed(
        FakeEvent(
            char="x",
            keysym="x",
        )
    )

    assert app.display_var.get() == ""
    assert result is None


def test_keyboard_full_expression():
    app = create_app()

    for character in "5*-2":
        app.key_pressed(
            FakeEvent(
                char=character,
                keysym=character,
            )
        )

    assert app.display_var.get() == "5*-2"

    with patch.object(
        app,
        "save",
    ):
        app.key_pressed(
            FakeEvent(
                keysym="Return",
            )
        )

    assert app.display_var.get() == "-10"


def test_keyboard_result_chaining():
    app = create_app()

    app.display_var.set("2+2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.key_pressed(
        FakeEvent(
            char="+",
            keysym="plus",
        )
    )

    app.key_pressed(
        FakeEvent(
            char="6",
            keysym="6",
        )
    )

    assert app.display_var.get() == "4+6"

    with patch.object(
        app,
        "save",
    ):
        app.key_pressed(
            FakeEvent(
                keysym="Return",
            )
        )

    assert app.display_var.get() == "10"


def test_pi_shortcut():
    app = create_app()

    result = app.pi_shortcut(None)

    assert app.display_var.get() == "pi"
    assert result == "break"


def test_e_shortcut():
    app = create_app()

    result = app.e_shortcut(None)

    assert app.display_var.get() == "e"
    assert result == "break"


def test_square_root_shortcut():
    app = create_app()

    app.display_var.set("144")

    result = app.sqrt_shortcut(None)

    assert app.display_var.get() == "sqrt(144)"
    assert result == "break"


def test_square_shortcut():
    app = create_app()

    app.display_var.set("12")

    app.square_shortcut(None)

    assert app.display_var.get() == "square(12)"


def test_reciprocal_shortcut():
    app = create_app()

    app.display_var.set("4")

    app.reciprocal_shortcut(None)

    assert app.display_var.get() == "reciprocal(4)"


def test_factorial_shortcut():
    app = create_app()

    app.display_var.set("5")

    app.factorial_shortcut(None)

    assert app.display_var.get() == "factorial(5)"


def test_log_shortcut():
    app = create_app()

    app.display_var.set("1000")

    app.log_shortcut(None)

    assert app.display_var.get() == "log(1000)"


def test_ln_shortcut():
    app = create_app()

    app.display_var.set("e")

    app.ln_shortcut(None)

    assert app.display_var.get() == "ln(e)"


def test_sin_shortcut():
    app = create_app()

    app.sin_shortcut(None)

    assert app.display_var.get() == "sin("


def test_inverse_sine_shortcut():
    app = create_app()

    app.asin_shortcut(None)

    assert app.display_var.get() == "asin("


def test_degree_mode_shortcut():
    app = create_app()

    app.angle_mode_var.set("radians")

    result = app.degree_mode_shortcut(None)

    assert app.angle_mode_var.get() == "degrees"
    assert result == "break"


def test_radian_mode_shortcut():
    app = create_app()

    app.angle_mode_var.set("degrees")

    result = app.radian_mode_shortcut(None)

    assert app.angle_mode_var.get() == "radians"
    assert result == "break"


def test_ans_shortcut():
    app = create_app()

    app.last_result = 42

    result = app.ans_shortcut(None)

    assert app.display_var.get() == "42"
    assert result == "break"


def test_update_mode_status_degrees():
    app = create_app()

    app.mode_status_var = FakeStringVar("RAD")
    app.angle_mode_var.set("degrees")

    app.update_mode_status()

    assert app.mode_status_var.get() == "DEG"


def test_update_mode_status_radians():
    app = create_app()

    app.mode_status_var = FakeStringVar("DEG")
    app.angle_mode_var.set("radians")

    app.update_mode_status()

    assert app.mode_status_var.get() == "RAD"


def test_degree_shortcut_updates_status():
    app = create_app()

    app.mode_status_var = FakeStringVar("RAD")

    app.degree_mode_shortcut(None)

    assert app.angle_mode_var.get() == "degrees"
    assert app.mode_status_var.get() == "DEG"


def test_radian_shortcut_updates_status():
    app = create_app()

    app.mode_status_var = FakeStringVar("DEG")
    app.angle_mode_var.set("degrees")

    app.radian_mode_shortcut(None)

    assert app.angle_mode_var.get() == "radians"
    assert app.mode_status_var.get() == "RAD"


def test_saved_angle_mode_restores_degrees():
    app = create_app()

    app.settings = {
        "angle_mode": "degrees",
        "geometry": "",
    }

    app.angle_mode_var.set(app.settings["angle_mode"])

    app.update_mode_status()

    assert app.angle_mode_var.get() == "degrees"
    assert app.mode_status_var.get() == "DEG"


def test_invalid_saved_angle_mode_defaults_to_radians():
    app = create_app()

    app.settings = {
        "angle_mode": "invalid",
        "geometry": "",
    }

    saved_mode = app.settings.get(
        "angle_mode",
        "radians",
    )

    if saved_mode not in {
        "degrees",
        "radians",
    }:
        saved_mode = "radians"

    assert saved_mode == "radians"


def test_update_saved_settings():
    app = create_app()

    app.root = MagicMock()
    app.root.geometry.return_value = "700x850+250+100"

    app.settings = {
        "angle_mode": "radians",
        "geometry": "",
    }

    app.angle_mode_var.set("degrees")

    app.update_saved_settings()

    assert app.settings["angle_mode"] == "degrees"
    assert app.settings["geometry"] == "700x850+250+100"


def test_reset_window_layout_confirmed():
    app = create_app()

    app.root = MagicMock()

    app.settings = {
        "angle_mode": "degrees",
        "geometry": "700x900+100+100",
    }

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=True,
        ),
        patch.object(
            app,
            "center_window",
        ) as mock_center,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.reset_window_layout()

    assert app.settings["geometry"] == ""

    mock_center.assert_called_once_with(
        app.root,
        560,
        790,
    )

    mock_save.assert_called_once()


def test_reset_window_layout_cancelled():
    app = create_app()

    app.root = MagicMock()

    app.settings = {
        "angle_mode": "degrees",
        "geometry": "700x900+100+100",
    }

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=False,
        ),
        patch.object(
            app,
            "center_window",
        ) as mock_center,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.reset_window_layout()

    assert app.settings["geometry"] == "700x900+100+100"

    mock_center.assert_not_called()
    mock_save.assert_not_called()


def test_reset_preferences_confirmed():
    app = create_app()

    app.root = MagicMock()

    app.settings = {
        "angle_mode": "degrees",
        "geometry": "700x900+100+100",
    }

    app.angle_mode_var.set("degrees")

    app.mode_status_var.set("DEG")

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=True,
        ),
        patch.object(
            app,
            "center_window",
        ) as mock_center,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.reset_preferences()

    assert app.settings["angle_mode"] == "radians"

    assert app.settings["geometry"] == ""

    assert app.angle_mode_var.get() == "radians"

    assert app.mode_status_var.get() == "RAD"

    mock_center.assert_called_once_with(
        app.root,
        560,
        790,
    )

    mock_save.assert_called_once()


def test_reset_preferences_keeps_history_and_memory():
    app = create_app()

    app.root = MagicMock()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2+2",
            "result": 4,
        }
    ]

    app.memory = {
        "answer": 42,
    }

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=True,
        ),
        patch.object(
            app,
            "center_window",
        ),
        patch.object(
            app,
            "save",
        ),
    ):
        app.reset_preferences()

    assert len(app.history) == 1
    assert app.memory == {
        "answer": 42,
    }
