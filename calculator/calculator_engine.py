import ast
import math
import operator
from collections.abc import Callable
from typing import Literal

Number = int | float
AngleMode = Literal["radians", "degrees"]


OPERATORS: dict[
    type[ast.operator] | type[ast.unaryop],
    Callable[..., Number],
] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


CONSTANTS: dict[str, Number] = {
    "pi": math.pi,
    "e": math.e,
}


FUNCTIONS: dict[
    str,
    Callable[[Number], Number],
] = {
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "square": lambda value: value**2,
    "reciprocal": lambda value: 1 / value,
    "pow10": lambda value: 10**value,
    "exp": math.exp,
}


TRIG_FUNCTIONS: dict[
    str,
    Callable[[float], float],
] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}


INVERSE_TRIG_FUNCTIONS: dict[
    str,
    Callable[[float], float],
] = {
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
}


def convert_angle(
    angle: Number,
    angle_mode: AngleMode,
) -> float:
    if angle_mode == "degrees":
        return math.radians(angle)

    return float(angle)


def convert_inverse_angle(
    angle: float,
    angle_mode: AngleMode,
) -> float:
    if angle_mode == "degrees":
        return math.degrees(angle)

    return angle


def factorial(value: Number) -> int:
    if isinstance(value, float):
        if not value.is_integer():
            raise ValueError("Factorial requires a whole number")

        value = int(value)

    if value < 0:
        raise ValueError("Factorial requires a non-negative number")

    return math.factorial(value)


def evaluate_node(
    node: ast.AST,
    angle_mode: AngleMode = "radians",
) -> Number:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError("Boolean values are not supported")

        if isinstance(
            node.value,
            (int, float),
        ):
            return node.value

        raise ValueError("Only numeric constants are supported")

    if isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]

        raise ValueError("Invalid constant")

    if isinstance(node, ast.BinOp):
        binary_operator_type = type(node.op)

        if binary_operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        left = evaluate_node(
            node.left,
            angle_mode,
        )

        right = evaluate_node(
            node.right,
            angle_mode,
        )

        operation = OPERATORS[binary_operator_type]

        return operation(
            left,
            right,
        )

    if isinstance(node, ast.UnaryOp):
        unary_operator_type = type(node.op)

        if unary_operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        operand = evaluate_node(
            node.operand,
            angle_mode,
        )

        operation = OPERATORS[unary_operator_type]

        return operation(operand)

    if isinstance(node, ast.Call):
        if not isinstance(
            node.func,
            ast.Name,
        ):
            raise ValueError("Invalid function")

        function_name = node.func.id

        valid_function = (
            function_name in FUNCTIONS
            or function_name in TRIG_FUNCTIONS
            or function_name in INVERSE_TRIG_FUNCTIONS
            or function_name == "factorial"
        )

        if not valid_function:
            raise ValueError("Invalid function")

        if len(node.args) != 1:
            raise ValueError("Scientific functions require one argument")

        if node.keywords:
            raise ValueError("Keyword arguments are not supported")

        argument = evaluate_node(
            node.args[0],
            angle_mode,
        )

        if function_name in TRIG_FUNCTIONS:
            converted_angle = convert_angle(
                argument,
                angle_mode,
            )

            trig_function = TRIG_FUNCTIONS[function_name]

            return trig_function(converted_angle)

        if function_name in INVERSE_TRIG_FUNCTIONS:
            inverse_function = INVERSE_TRIG_FUNCTIONS[function_name]

            result = inverse_function(float(argument))

            return convert_inverse_angle(
                result,
                angle_mode,
            )

        if function_name == "factorial":
            return factorial(argument)

        function = FUNCTIONS[function_name]

        return function(argument)

    raise ValueError("Invalid expression")


def calculate_expression(
    expression: str,
    angle_mode: AngleMode = "radians",
) -> Number:
    expression = expression.strip()

    tree = ast.parse(
        expression,
        mode="eval",
    )

    result = evaluate_node(
        tree.body,
        angle_mode,
    )

    if isinstance(result, complex):
        raise TypeError("Complex numbers are not supported")

    return result


def format_number(
    number: Number,
) -> Number:
    if isinstance(number, float):
        if math.isclose(
            number,
            0.0,
            abs_tol=1e-12,
        ):
            return 0

        nearest_integer = round(number)

        if math.isclose(
            number,
            nearest_integer,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            return int(nearest_integer)

    return number
