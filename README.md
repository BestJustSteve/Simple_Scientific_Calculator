# Simple Scientific Calculator

A desktop scientific calculator built with Python and Tkinter.

The application supports standard arithmetic, scientific functions, keyboard shortcuts, calculation history, named memory values, persistent preferences, and safe expression evaluation using Python's AST module.

## Features

### Standard Calculator Operations

- Addition
- Subtraction
- Multiplication
- Division
- Floor division
- Modulus
- Exponentiation
- Parentheses
- Decimal values
- Negative numbers

### Scientific Functions

- `sin`
- `cos`
- `tan`
- `asin`
- `acos`
- `atan`
- Square root
- Square
- Reciprocal
- Factorial
- Base-10 logarithm
- Natural logarithm
- Powers of 10
- Exponential function
- π
- e

### Angle Modes

The calculator supports:

- Radians
- Degrees

The active mode is displayed in the status bar.

The selected angle mode is remembered when the application is closed.

### Smart Expression Input

The calculator includes input handling designed to make expression entry easier and safer.

Examples include:

- Automatic parenthesis completion
- Smart closing-parenthesis handling
- Operator replacement
- Negative values after operators
- Decimal input protection
- Implicit multiplication
- Constant detection
- Function detection
- ANS operand insertion
- Memory operand insertion
- Invalid operator-chain cleanup

Examples:

```text
2π
```

is automatically entered internally as:

```text
2*pi
```

and:

```text
(2)(3)
```

is treated as:

```text
(2)*(3)
```

If the previous answer is `42`:

```text
2
ANS
```

becomes:

```text
2*42
```

while:

```text
5+
ANS
```

becomes:

```text
5+42
```

### Calculation History

The calculator stores calculation history locally.

The History window includes:

- Timestamp
- Expression
- Result
- Scrollable history table
- Use Result action
- Double-click result reuse
- Clear History option

Newest calculations are displayed first.

### Memory

Results can be stored under custom names.

The Memory window includes:

- Named values
- Sorted memory table
- Use stored value
- Double-click stored value
- Delete stored value

Memory values are persisted between application sessions.

### Persistent Preferences

The calculator remembers:

- Angle mode
- Main window size
- Main window position

The next time the calculator opens, these preferences are restored automatically.

### Settings

The Settings menu includes:

#### Reset Window Layout

Restores the calculator window to its default size and centered position.

This does not affect:

- Angle mode
- History
- Memory

#### Reset Preferences

Restores:

- Radian mode
- Default window size
- Default window position

History and memory are preserved.

### Keyboard Support

Normal keyboard input can be used for calculations.

Supported direct input includes:

```text
0-9
+
-
*
/
%
.
(
)
```

Typing:

```text
**
```

creates exponentiation.

Typing:

```text
//
```

creates floor division.

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Enter | Calculate |
| Numpad Enter | Calculate |
| Backspace | Delete last character |
| Escape | Clear display |
| Delete | Clear display |
| Ctrl+A | Clear display |
| Ctrl+L | Clear display |
| Ctrl+P | Insert π |
| Ctrl+E | Insert e |
| Ctrl+R | Square root |
| Ctrl+Q | Square |
| Ctrl+I | Reciprocal |
| Ctrl+F | Factorial |
| Ctrl+G | Base-10 logarithm |
| Ctrl+N | Natural logarithm |
| Ctrl+1 | sin |
| Ctrl+2 | cos |
| Ctrl+3 | tan |
| Ctrl+4 | asin |
| Ctrl+5 | acos |
| Ctrl+6 | atan |
| Ctrl+D | Degree mode |
| Ctrl+T | Radian mode |
| Ctrl+Space | Insert previous answer |
| Ctrl+H | Open History |
| Ctrl+M | Open Memory |
| Ctrl+S | Save last result to Memory |
| F1 | Open Keyboard Shortcuts |

## Safe Expression Evaluation

The calculator does not use unrestricted Python `eval()`.

Expressions are parsed using Python's `ast` module and only approved operations, constants, and scientific functions are evaluated.

Unsupported syntax is rejected.

Examples of rejected input include:

```python
import os
```

```python
__import__("os")
```

```python
object.attribute
```

```python
[1, 2, 3]
```

```python
{"a": 1}
```

This keeps calculator expressions isolated from arbitrary Python execution.

## Requirements

- Python 3.12 or newer
- Tkinter

Development tools used by the project include:

- pytest
- pytest-cov
- Ruff
- mypy
- pre-commit

## Installation

Clone the repository:

```bash
git clone https://github.com/BestJustSteve/Simple_Scientific_Calculator.git
```

Enter the project directory:

```bash
cd Simple_Scientific_Calculator
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Or activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project requirements:

```bash
python -m pip install -r requirements.txt
```

## Running the Calculator

Run:

```bash
python main.py
```

## Running Tests

Run the full test suite:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest --cov=calculator --cov-report=term-missing
```

## Code Quality

Run Ruff:

```bash
python -m ruff check . --fix
python -m ruff check .
python -m ruff format .
```

Run mypy:

```bash
python -m mypy calculator
```

Run pre-commit checks:

```bash
python -m pre_commit run --all-files
```

A full local verification sequence is:

```bash
python -m ruff check . --fix
python -m ruff check .
python -m ruff format .
python -m mypy calculator
python -m pytest -v
python -m pytest --cov=calculator --cov-report=term-missing
python -m pre_commit run --all-files
```

## Persistent Data

Application data is stored in a JSON file.

On Windows, the calculator stores its data under:

```text
%LOCALAPPDATA%\SimpleScientificCalculator\
```

The file is:

```text
calculator_data.json
```

It stores:

- Calculation history
- Named memory values
- Last result
- Angle mode
- Window geometry

An example structure is:

```json
{
    "history": [],
    "memory": {},
    "last_result": null,
    "settings": {
        "angle_mode": "radians",
        "geometry": "560x790+680+145"
    }
}
```

If the file does not exist, the calculator creates its data automatically.

If saved JSON is missing newer settings fields, default values are used.

## Project Structure

```text
Simple_Scientific_Calculator/
├── calculator/
│   ├── __init__.py
│   ├── calculator_engine.py
│   ├── gui.py
│   ├── gui_helpers.py
│   ├── storage.py
│   └── version.py
├── tests/
│   ├── test_calculator_engine.py
│   ├── test_gui.py
│   ├── test_gui_helpers.py
│   ├── test_history_memory_windows.py
│   ├── test_keyboard_shortcuts_window.py
│   ├── test_storage.py
│   └── test_window_geometry.py
├── .github/
│   └── workflows/
│       ├── release.yml
│       └── tests.yml
├── .pre-commit-config.yaml
├── .gitignore
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Architecture

### `calculator/calculator_engine.py`

Contains calculator logic and safe AST-based expression evaluation.

This layer does not depend on Tkinter.

### `calculator/gui.py`

Contains the Tkinter desktop interface and user interaction logic.

### `calculator/gui_helpers.py`

Contains smaller display and formatting helpers used by the GUI.

### `calculator/storage.py`

Handles JSON persistence for:

- History
- Memory
- Last result
- Application preferences

### `calculator/version.py`

Contains the application version.

Current version:

```text
0.1.0
```

## Continuous Integration

GitHub Actions is used to run automated project checks.

The test workflow verifies the project when changes are pushed or submitted through pull requests.

The repository also contains a release workflow for packaged releases.

## Development

Before committing changes, run:

```bash
python -m ruff check . --fix
python -m ruff check .
python -m ruff format .
python -m mypy calculator
python -m pytest -v
python -m pytest --cov=calculator --cov-report=term-missing
python -m pre_commit run --all-files
```

## Version

Current development version:

```text
0.1.0
```

## License

No license has been selected yet.
