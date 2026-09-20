from unittest.mock import MagicMock, patch

import pytest

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
    app = CalculatorApp.__new__(
        CalculatorApp
    )

    app.display_var = FakeStringVar()
    app.previous_var = FakeStringVar()
    app.angle_mode_var = FakeStringVar(
        "radians"
    )

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
    assert app.last_result == 14


def test_calculate_decimal():
    app = create_app()

    app.display_var.set("5 / 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "2.5"
    assert app.last_result == 2.5


def test_calculate_sine_in_degrees():
    app = create_app()

    app.angle_mode_var.set("degrees")
    app.display_var.set("sin(90)")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(
        app.display_var.get()
    ) == pytest.approx(1)


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


def test_calculate_cosine_90_degrees_formats_as_zero():
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

    app.angle_mode_var.set("radians")
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


def test_calculate_pi_expression():
    app = create_app()

    app.display_var.set("2 * pi")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(
        app.display_var.get()
    ) == pytest.approx(
        2 * 3.141592653589793
    )


def test_calculate_e_constant():
    app = create_app()

    app.display_var.set("e")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(
        app.display_var.get()
    ) == pytest.approx(
        2.718281828459045
    )


def test_insert_sine_function():
    app = create_app()

    app.button_click("sin(")

    assert app.display_var.get() == "sin("


def test_insert_cosine_function():
    app = create_app()

    app.button_click("cos(")

    assert app.display_var.get() == "cos("


def test_insert_tangent_function():
    app = create_app()

    app.button_click("tan(")

    assert app.display_var.get() == "tan("


def test_insert_inverse_sine():
    app = create_app()

    app.button_click("asin(")

    assert app.display_var.get() == "asin("


def test_insert_inverse_cosine():
    app = create_app()

    app.button_click("acos(")

    assert app.display_var.get() == "acos("


def test_insert_inverse_tangent():
    app = create_app()

    app.button_click("atan(")

    assert app.display_var.get() == "atan("


def test_insert_pi_constant():
    app = create_app()

    app.button_click("pi")

    assert app.display_var.get() == "pi"


def test_insert_e_constant():
    app = create_app()

    app.button_click("e")

    assert app.display_var.get() == "e"


def test_build_scientific_expression_with_buttons():
    app = create_app()

    app.button_click("sin(")
    app.button_click("90")
    app.button_click(")")

    assert app.display_var.get() == "sin(90)"


def test_apply_square_to_current_expression():
    app = create_app()

    app.display_var.set("12")

    app.apply_to_current_expression(
        "square"
    )

    assert app.display_var.get() == "square(12)"


def test_apply_square_to_full_expression():
    app = create_app()

    app.display_var.set("2 + 3")

    app.apply_to_current_expression(
        "square"
    )

    assert app.display_var.get() == "square(2 + 3)"


def test_apply_reciprocal():
    app = create_app()

    app.display_var.set("4")

    app.apply_to_current_expression(
        "reciprocal"
    )

    assert app.display_var.get() == "reciprocal(4)"


def test_apply_factorial():
    app = create_app()

    app.display_var.set("5")

    app.apply_to_current_expression(
        "factorial"
    )

    assert app.display_var.get() == "factorial(5)"


def test_apply_square_root():
    app = create_app()

    app.display_var.set("144")

    app.apply_to_current_expression(
        "sqrt"
    )

    assert app.display_var.get() == "sqrt(144)"


def test_apply_log():
    app = create_app()

    app.display_var.set("1000")

    app.apply_to_current_expression(
        "log"
    )

    assert app.display_var.get() == "log(1000)"


def test_apply_ln():
    app = create_app()

    app.display_var.set("e")

    app.apply_to_current_expression(
        "ln"
    )

    assert app.display_var.get() == "ln(e)"


def test_apply_power_of_ten():
    app = create_app()

    app.display_var.set("3")

    app.apply_to_current_expression(
        "pow10"
    )

    assert app.display_var.get() == "pow10(3)"


def test_apply_exponential():
    app = create_app()

    app.display_var.set("1")

    app.apply_to_current_expression(
        "exp"
    )

    assert app.display_var.get() == "exp(1)"


def test_apply_function_to_empty_display():
    app = create_app()

    app.apply_to_current_expression(
        "sqrt"
    )

    assert app.display_var.get() == "sqrt("
    assert app.just_calculated is False


def test_square_button_then_calculate():
    app = create_app()

    app.display_var.set("12")

    app.apply_to_current_expression(
        "square"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "144"


def test_reciprocal_button_then_calculate():
    app = create_app()

    app.display_var.set("4")

    app.apply_to_current_expression(
        "reciprocal"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "0.25"


def test_factorial_button_then_calculate():
    app = create_app()

    app.display_var.set("5")

    app.apply_to_current_expression(
        "factorial"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "120"


def test_sqrt_button_then_calculate():
    app = create_app()

    app.display_var.set("144")

    app.apply_to_current_expression(
        "sqrt"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"


def test_log_button_then_calculate():
    app = create_app()

    app.display_var.set("1000")

    app.apply_to_current_expression(
        "log"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "3"


def test_ln_button_then_calculate():
    app = create_app()

    app.display_var.set("e")

    app.apply_to_current_expression(
        "ln"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"


def test_pow10_button_then_calculate():
    app = create_app()

    app.display_var.set("3")

    app.apply_to_current_expression(
        "pow10"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1000"


def test_exp_button_then_calculate():
    app = create_app()

    app.display_var.set("1")

    app.apply_to_current_expression(
        "exp"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert float(
        app.display_var.get()
    ) == pytest.approx(
        2.718281828459045
    )


def test_number_starts_new_expression_after_calculation():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "4"
    assert app.just_calculated is True

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
    assert app.just_calculated is False


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


def test_power_operator_continues_after_result():
    app = create_app()

    app.display_var.set("3")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("**")
    app.button_click("2")

    assert app.display_var.get() == "3**2"


def test_number_replaces_previous_result():
    app = create_app()

    app.display_var.set("10 / 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("9")

    assert app.display_var.get() == "9"


def test_scientific_prefix_starts_fresh_after_result():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("sin(")

    assert app.display_var.get() == "sin("


def test_scientific_operation_uses_previous_result():
    app = create_app()

    app.display_var.set("12")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.apply_to_current_expression(
        "square"
    )

    assert app.display_var.get() == "square(12)"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "144"


def test_square_root_previous_result():
    app = create_app()

    app.display_var.set("12")

    app.apply_to_current_expression(
        "square"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "144"

    app.apply_to_current_expression(
        "sqrt"
    )

    assert app.display_var.get() == "sqrt(144)"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"


def test_clear_resets_calculation_state():
    app = create_app()

    app.just_calculated = True
    app.display_var.set("42")

    app.clear_display()

    assert app.just_calculated is False
    assert app.display_var.get() == ""


def test_backspace_resets_calculation_state():
    app = create_app()

    app.just_calculated = True
    app.display_var.set("42")

    app.backspace()

    assert app.just_calculated is False
    assert app.display_var.get() == "4"


def test_calculate_empty_expression():
    app = create_app()

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.calculate()

    mock_save.assert_not_called()

    assert app.history == []
    assert app.last_result is None


def test_calculate_division_by_zero():
    app = create_app()

    app.display_var.set("10 / 0")

    with (
        patch(
            "calculator.gui.messagebox.showerror"
        ) as mock_error,
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

    assert app.history == []
    assert app.last_result is None


def test_calculate_invalid_expression():
    app = create_app()

    app.display_var.set("2 +")

    with (
        patch(
            "calculator.gui.messagebox.showerror"
        ) as mock_error,
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
        patch(
            "calculator.gui.messagebox.showerror"
        ) as mock_error,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.calculate()

    mock_error.assert_called_once_with(
        "Error",
        "That number is too large.",
    )

    mock_save.assert_not_called()


def test_use_last_result():
    app = create_app()

    app.last_result = 42

    app.use_last_result()

    assert app.display_var.get() == "42"


def test_use_decimal_last_result():
    app = create_app()

    app.last_result = 2.5

    app.use_last_result()

    assert app.display_var.get() == "2.5"


def test_use_last_result_when_none():
    app = create_app()

    with patch(
        "calculator.gui.messagebox.showinfo"
    ) as mock_info:
        app.use_last_result()

    mock_info.assert_called_once_with(
        "Last Result",
        "No previous result is available.",
    )

    assert app.display_var.get() == ""


def test_clear_history():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=True,
        ),
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.clear_history()

    assert app.history == []

    mock_save.assert_called_once()


def test_clear_history_cancelled():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    with (
        patch(
            "calculator.gui.messagebox.askyesno",
            return_value=False,
        ),
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.clear_history()

    assert len(app.history) == 1

    mock_save.assert_not_called()


def test_clear_empty_history():
    app = create_app()

    with patch(
        "calculator.gui.messagebox.showinfo"
    ) as mock_info:
        app.clear_history()

    mock_info.assert_called_once_with(
        "History",
        "History is already empty.",
    )


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

    fake_last_result = 4

    with patch(
        "calculator.gui.load_data",
        return_value=(
            fake_history,
            fake_memory,
            fake_last_result,
        ),
    ):
        app.load_saved_data()

    assert app.history == fake_history
    assert app.memory == fake_memory
    assert app.last_result == 4


def test_save():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    app.memory = {
        "answer": 4,
    }

    app.last_result = 4

    with patch(
        "calculator.gui.save_data"
    ) as mock_save_data:
        app.save()

    mock_save_data.assert_called_once_with(
        app.history,
        app.memory,
        app.last_result,
    )


def test_save_oserror():
    app = create_app()

    with (
        patch(
            "calculator.gui.save_data",
            side_effect=OSError,
        ),
        patch(
            "calculator.gui.messagebox.showerror"
        ) as mock_error,
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


def test_use_decimal_memory_value():
    app = create_app()

    mock_window = MagicMock()

    app.use_memory_value(
        2.5,
        mock_window,
    )

    assert app.display_var.get() == "2.5"

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

    app.memory = {}

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


def test_complete_one_missing_parenthesis():
    app = create_app()

    result = app.complete_parentheses(
        "sin(90"
    )

    assert result == "sin(90)"


def test_complete_multiple_missing_parentheses():
    app = create_app()

    result = app.complete_parentheses(
        "sqrt(square(12"
    )

    assert result == "sqrt(square(12))"


def test_complete_parentheses_does_not_change_complete_expression():
    app = create_app()

    result = app.complete_parentheses(
        "sin(90)"
    )

    assert result == "sin(90)"


def test_complete_parentheses_does_not_change_expression_without_parentheses():
    app = create_app()

    result = app.complete_parentheses(
        "2 + 2"
    )

    assert result == "2 + 2"


def test_complete_parentheses_does_not_remove_extra_closing_parenthesis():
    app = create_app()

    result = app.complete_parentheses(
        "sin(90))"
    )

    assert result == "sin(90))"


def test_calculate_auto_closes_sine():
    app = create_app()

    app.angle_mode_var.set(
        "degrees"
    )

    app.display_var.set(
        "sin(90"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"
    assert app.previous_var.get() == "sin(90) ="
    assert app.just_calculated is True


def test_calculate_auto_closes_cosine():
    app = create_app()

    app.angle_mode_var.set(
        "degrees"
    )

    app.display_var.set(
        "cos(180"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "-1"
    assert app.previous_var.get() == "cos(180) ="


def test_calculate_auto_closes_square_root():
    app = create_app()

    app.display_var.set(
        "sqrt(144"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"
    assert app.previous_var.get() == "sqrt(144) ="


def test_calculate_auto_closes_factorial():
    app = create_app()

    app.display_var.set(
        "factorial(5"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "120"
    assert app.previous_var.get() == "factorial(5) ="


def test_calculate_auto_closes_log():
    app = create_app()

    app.display_var.set(
        "log(1000"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "3"


def test_calculate_auto_closes_ln():
    app = create_app()

    app.display_var.set(
        "ln(e"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"


def test_calculate_auto_closes_nested_functions():
    app = create_app()

    app.display_var.set(
        "sqrt(square(12"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"
    assert (
        app.previous_var.get()
        == "sqrt(square(12)) ="
    )


def test_auto_completed_expression_is_saved_to_history():
    app = create_app()

    app.angle_mode_var.set(
        "degrees"
    )

    app.display_var.set(
        "sin(90"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert len(app.history) == 1
    assert (
        app.history[0]["expression"]
        == "sin(90)"
    )
    assert (
        app.history[0]["result"]
        == pytest.approx(1)
    )


def test_scientific_button_can_calculate_without_manual_closing_parenthesis():
    app = create_app()

    app.angle_mode_var.set(
        "degrees"
    )

    app.button_click(
        "sin("
    )
    app.button_click(
        "90"
    )

    assert (
        app.display_var.get()
        == "sin(90"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "1"


def test_nested_scientific_buttons_auto_complete():
    app = create_app()

    app.apply_to_current_expression(
        "square"
    )

    app.button_click(
        "12"
    )

    assert (
        app.display_var.get()
        == "square(12"
    )

    app.apply_to_current_expression(
        "sqrt"
    )

    assert (
        app.display_var.get()
        == "sqrt(square(12)"
    )

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "12"


def test_is_operator():
    app = create_app()

    assert app.is_operator("+") is True
    assert app.is_operator("-") is True
    assert app.is_operator("*") is True
    assert app.is_operator("/") is True
    assert app.is_operator("%") is True
    assert app.is_operator("//") is True
    assert app.is_operator("**") is True


def test_number_is_not_operator():
    app = create_app()

    assert app.is_operator("5") is False


def test_operator_replaces_previous_operator():
    app = create_app()

    app.display_var.set("5+")

    app.button_click("*")

    assert app.display_var.get() == "5*"


def test_division_replaces_addition():
    app = create_app()

    app.display_var.set("10+")

    app.button_click("/")

    assert app.display_var.get() == "10/"


def test_power_operator_replaces_previous_operator():
    app = create_app()

    app.display_var.set("5+")

    app.button_click("**")

    assert app.display_var.get() == "5**"


def test_floor_division_replaces_previous_operator():
    app = create_app()

    app.display_var.set("10*")

    app.button_click("//")

    assert app.display_var.get() == "10//"


def test_operator_replaces_power_operator():
    app = create_app()

    app.display_var.set("5**")

    app.button_click("/")

    assert app.display_var.get() == "5/"


def test_operator_replaces_floor_division():
    app = create_app()

    app.display_var.set("10//")

    app.button_click("+")

    assert app.display_var.get() == "10+"


def test_minus_can_start_expression():
    app = create_app()

    app.button_click("-")

    assert app.display_var.get() == "-"


def test_plus_cannot_start_expression():
    app = create_app()

    app.button_click("+")

    assert app.display_var.get() == ""


def test_multiplication_cannot_start_expression():
    app = create_app()

    app.button_click("*")

    assert app.display_var.get() == ""


def test_division_cannot_start_expression():
    app = create_app()

    app.button_click("/")

    assert app.display_var.get() == ""


def test_power_cannot_start_expression():
    app = create_app()

    app.button_click("**")

    assert app.display_var.get() == ""


def test_floor_division_cannot_start_expression():
    app = create_app()

    app.button_click("//")

    assert app.display_var.get() == ""


def test_minus_after_multiplication_starts_negative_number():
    app = create_app()

    app.display_var.set("5*")

    app.button_click("-")

    assert app.display_var.get() == "5*-"


def test_minus_after_division_starts_negative_number():
    app = create_app()

    app.display_var.set("10/")

    app.button_click("-")

    assert app.display_var.get() == "10/-"


def test_minus_after_modulus_starts_negative_number():
    app = create_app()

    app.display_var.set("10%")

    app.button_click("-")

    assert app.display_var.get() == "10%-"


def test_minus_after_power_starts_negative_number():
    app = create_app()

    app.display_var.set("2**")

    app.button_click("-")

    assert app.display_var.get() == "2**-"


def test_minus_after_floor_division_starts_negative_number():
    app = create_app()

    app.display_var.set("10//")

    app.button_click("-")

    assert app.display_var.get() == "10//-"


def test_negative_number_expression_calculates():
    app = create_app()

    app.button_click("5")
    app.button_click("*")
    app.button_click("-")
    app.button_click("2")

    assert app.display_var.get() == "5*-2"

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "-10"


def test_negative_division_expression_calculates():
    app = create_app()

    app.button_click("10")
    app.button_click("/")
    app.button_click("-")
    app.button_click("2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "-5"


def test_repeated_operator_changes_operator():
    app = create_app()

    app.button_click("5")
    app.button_click("+")
    app.button_click("*")

    assert app.display_var.get() == "5*"


def test_multiple_operator_replacements():
    app = create_app()

    app.button_click("5")
    app.button_click("+")
    app.button_click("*")
    app.button_click("/")

    assert app.display_var.get() == "5/"


def test_operator_chaining_after_result_still_works():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("+")

    assert app.display_var.get() == "4+"

    app.button_click("*")

    assert app.display_var.get() == "4*"


def test_operator_after_result_can_continue_calculation():
    app = create_app()

    app.display_var.set("2 + 2")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("*")
    app.button_click("5")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "20"


def test_minus_after_result_continues_subtraction():
    app = create_app()

    app.display_var.set("10")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    app.button_click("-")
    app.button_click("3")

    with patch.object(
        app,
        "save",
    ):
        app.calculate()

    assert app.display_var.get() == "7"
