import math

import pytest

from calculator.calculator_engine import (
    calculate_expression,
    convert_angle,
    factorial,
    format_number,
)


def test_nested_parentheses():
    assert (
        calculate_expression(
            "((2 + 3) * (4 + 1))"
        )
        == 25
    )


def test_multiple_operations():
    assert (
        calculate_expression(
            "2 + 3 * 4 - 5"
        )
        == 9
    )


def test_negative_parentheses():
    assert (
        calculate_expression(
            "-(2 + 3)"
        )
        == -5
    )


def test_unary_plus():
    assert (
        calculate_expression(
            "+5"
        )
        == 5
    )


def test_decimal_division():
    assert (
        calculate_expression(
            "5 / 2"
        )
        == 2.5
    )


def test_decimal_multiplication():
    assert (
        calculate_expression(
            "2.5 * 4"
        )
        == 10
    )


def test_power_precedence():
    assert (
        calculate_expression(
            "2 + 3 ** 2"
        )
        == 11
    )


def test_parentheses_override_precedence():
    assert (
        calculate_expression(
            "(2 + 3) ** 2"
        )
        == 25
    )


def test_floor_division_negative_number():
    assert (
        calculate_expression(
            "-7 // 2"
        )
        == -4
    )


def test_modulus_negative_number():
    assert (
        calculate_expression(
            "-7 % 2"
        )
        == 1
    )


def test_empty_expression():
    with pytest.raises(
        SyntaxError
    ):
        calculate_expression("")


def test_incomplete_expression():
    with pytest.raises(
        SyntaxError
    ):
        calculate_expression(
            "2 +"
        )


def test_double_operator_invalid():
    with pytest.raises(
        SyntaxError
    ):
        calculate_expression(
            "2 ** ** 3"
        )


def test_unknown_name_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "unknown"
        )


def test_function_call_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "abs(5)"
        )


def test_import_call_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "__import__('os')"
        )


def test_attribute_access_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "os.system('test')"
        )


def test_list_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "[1, 2, 3]"
        )


def test_dictionary_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "{'a': 1}"
        )


def test_comparison_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "1 < 2"
        )


def test_boolean_expression_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "True"
        )


def test_string_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "'hello'"
        )


def test_division_by_zero():
    with pytest.raises(
        ZeroDivisionError
    ):
        calculate_expression(
            "10 / 0"
        )


def test_floor_division_by_zero():
    with pytest.raises(
        ZeroDivisionError
    ):
        calculate_expression(
            "10 // 0"
        )


def test_modulus_by_zero():
    with pytest.raises(
        ZeroDivisionError
    ):
        calculate_expression(
            "10 % 0"
        )


def test_format_whole_float():
    assert (
        format_number(5.0)
        == 5
    )


def test_format_decimal():
    assert (
        format_number(5.5)
        == 5.5
    )


def test_format_integer():
    assert (
        format_number(5)
        == 5
    )


def test_large_power():
    assert (
        calculate_expression(
            "2 ** 100"
        )
        == 2**100
    )


def test_whitespace_expression():
    assert (
        calculate_expression(
            "  10 + 5  "
        )
        == 15
    )


def test_nested_unary_minus():
    assert (
        calculate_expression(
            "--5"
        )
        == 5
    )


def test_fractional_power():
    assert (
        calculate_expression(
            "9 ** 0.5"
        )
        == 3
    )


def test_complex_result_is_not_supported():
    with pytest.raises(
        TypeError
    ):
        calculate_expression(
            "(-1) ** 0.5"
        )


def test_unsupported_binary_operator_is_rejected():
    with pytest.raises(
        ValueError,
        match="Invalid operator",
    ):
        calculate_expression(
            "1 << 2"
        )


def test_unsupported_unary_operator_is_rejected():
    with pytest.raises(
        ValueError,
        match="Invalid operator",
    ):
        calculate_expression(
            "~5"
        )


def test_square_root():
    assert (
        calculate_expression(
            "sqrt(9)"
        )
        == 3
    )


def test_square_root_decimal():
    assert calculate_expression(
        "sqrt(2)"
    ) == pytest.approx(
        math.sqrt(2)
    )


def test_pi_constant():
    assert calculate_expression(
        "pi"
    ) == pytest.approx(
        math.pi
    )


def test_e_constant():
    assert calculate_expression(
        "e"
    ) == pytest.approx(
        math.e
    )


def test_pi_in_expression():
    assert calculate_expression(
        "2 * pi"
    ) == pytest.approx(
        2 * math.pi
    )


def test_sine():
    assert calculate_expression(
        "sin(0)"
    ) == pytest.approx(0)


def test_cosine():
    assert calculate_expression(
        "cos(0)"
    ) == pytest.approx(1)


def test_tangent():
    assert calculate_expression(
        "tan(0)"
    ) == pytest.approx(0)


def test_nested_scientific_function():
    assert (
        calculate_expression(
            "sqrt(16) + 2"
        )
        == 6
    )


def test_scientific_function_with_expression():
    assert (
        calculate_expression(
            "sqrt(9 + 7)"
        )
        == 4
    )


def test_unknown_constant_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "tau"
        )


def test_unknown_function_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "abs(5)"
        )


def test_scientific_function_requires_one_argument():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "sqrt()"
        )


def test_scientific_function_rejects_multiple_arguments():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "sqrt(4, 9)"
        )


def test_scientific_function_rejects_keyword_arguments():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "sqrt(x=9)"
        )


def test_attribute_function_call_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "math.sqrt(9)"
        )


def test_negative_square_root_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "sqrt(-1)"
        )


def test_sine_radians():
    assert calculate_expression(
        "sin(pi / 2)",
        "radians",
    ) == pytest.approx(1)


def test_cosine_radians():
    assert calculate_expression(
        "cos(pi)",
        "radians",
    ) == pytest.approx(-1)


def test_tangent_radians():
    assert calculate_expression(
        "tan(pi / 4)",
        "radians",
    ) == pytest.approx(1)


def test_sine_degrees():
    assert calculate_expression(
        "sin(90)",
        "degrees",
    ) == pytest.approx(1)


def test_cosine_degrees():
    assert calculate_expression(
        "cos(180)",
        "degrees",
    ) == pytest.approx(-1)


def test_tangent_degrees():
    assert calculate_expression(
        "tan(45)",
        "degrees",
    ) == pytest.approx(1)


def test_degree_mode_expression():
    assert calculate_expression(
        "sin(30) + cos(60)",
        "degrees",
    ) == pytest.approx(1)


def test_radian_mode_is_default():
    assert calculate_expression(
        "sin(pi / 2)"
    ) == pytest.approx(1)


def test_square_root_ignores_angle_mode():
    assert (
        calculate_expression(
            "sqrt(81)",
            "degrees",
        )
        == 9
    )


def test_constant_expression_in_degree_mode():
    assert calculate_expression(
        "2 * pi",
        "degrees",
    ) == pytest.approx(
        2 * math.pi
    )


def test_convert_degrees_to_radians():
    assert convert_angle(
        180,
        "degrees",
    ) == pytest.approx(
        math.pi
    )


def test_convert_radians_unchanged():
    assert convert_angle(
        math.pi,
        "radians",
    ) == pytest.approx(
        math.pi
    )


def test_format_tiny_number_as_zero():
    assert (
        format_number(
            6.123233995736766e-17
        )
        == 0
    )


def test_format_nearly_positive_integer():
    assert (
        format_number(
            0.9999999999999999
        )
        == 1
    )


def test_format_nearly_negative_integer():
    assert (
        format_number(
            -1.0000000000000002
        )
        == -1
    )


def test_format_non_integer_scientific_result():
    assert format_number(
        0.7071067811865476
    ) == pytest.approx(
        0.7071067811865476
    )


def test_log_base_10():
    assert calculate_expression(
        "log(1000)"
    ) == pytest.approx(3)


def test_natural_log():
    assert calculate_expression(
        "ln(e)"
    ) == pytest.approx(1)


def test_square():
    assert calculate_expression(
        "square(12)"
    ) == 144


def test_reciprocal():
    assert calculate_expression(
        "reciprocal(4)"
    ) == pytest.approx(0.25)


def test_reciprocal_zero_is_rejected():
    with pytest.raises(
        ZeroDivisionError
    ):
        calculate_expression(
            "reciprocal(0)"
        )


def test_power_of_ten():
    assert calculate_expression(
        "pow10(3)"
    ) == 1000


def test_exponential():
    assert calculate_expression(
        "exp(1)"
    ) == pytest.approx(
        math.e
    )


def test_factorial():
    assert calculate_expression(
        "factorial(5)"
    ) == 120


def test_factorial_zero():
    assert calculate_expression(
        "factorial(0)"
    ) == 1


def test_factorial_whole_float():
    assert calculate_expression(
        "factorial(5.0)"
    ) == 120


def test_factorial_decimal_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "factorial(5.5)"
        )


def test_factorial_negative_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "factorial(-1)"
        )


def test_asin_radians():
    assert calculate_expression(
        "asin(1)"
    ) == pytest.approx(
        math.pi / 2
    )


def test_acos_radians():
    assert calculate_expression(
        "acos(0)"
    ) == pytest.approx(
        math.pi / 2
    )


def test_atan_radians():
    assert calculate_expression(
        "atan(1)"
    ) == pytest.approx(
        math.pi / 4
    )


def test_asin_degrees():
    assert calculate_expression(
        "asin(1)",
        "degrees",
    ) == pytest.approx(90)


def test_acos_degrees():
    assert calculate_expression(
        "acos(0)",
        "degrees",
    ) == pytest.approx(90)


def test_atan_degrees():
    assert calculate_expression(
        "atan(1)",
        "degrees",
    ) == pytest.approx(45)


def test_inverse_trig_invalid_domain():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "asin(2)"
        )


def test_log_zero_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "log(0)"
        )


def test_ln_negative_is_rejected():
    with pytest.raises(
        ValueError
    ):
        calculate_expression(
            "ln(-1)"
        )

def test_factorial_helper():
    assert factorial(6) == 720


def test_factorial_helper_decimal_rejected():
    with pytest.raises(
        ValueError
    ):
        factorial(2.5)
