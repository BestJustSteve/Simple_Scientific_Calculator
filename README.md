# Simple Scientific Calculator

A desktop calculator application built with Python and Tkinter.

Simple Scientific Calculator started as a basic command-line learning project and has grown into a structured Python application with a graphical interface, persistent storage, calculation history, named memory values, automated testing, static type checking, linting, code formatting, CI, and Windows executable builds.

Current application version:

```text
1.0.0
```

---

## Features

### Calculator

- Addition
- Subtraction
- Multiplication
- Division
- Floor division
- Modulus
- Exponents
- Parentheses
- Operator precedence
- Decimal calculations
- Positive and negative numbers
- Previous-result support

Supported operators:

| Operation | Operator | Example |
|---|---|---|
| Addition | `+` | `2 + 2` |
| Subtraction | `-` | `10 - 3` |
| Multiplication | `*` | `6 * 7` |
| Division | `/` | `10 / 4` |
| Floor division | `//` | `10 // 3` |
| Modulus | `%` | `10 % 3` |
| Exponent | `**` | `2 ** 8` |
| Parentheses | `()` | `(2 + 3) * 4` |

---

## Safe Expression Evaluation

The calculator does **not** use Python's raw `eval()` function.

Mathematical expressions are parsed with Python's Abstract Syntax Tree (`ast`) module.

Only specifically supported numeric operations are evaluated.

Expressions involving unsupported Python functionality are rejected, including:

- Variable names
- Function calls
- Imports
- Attribute access
- Lists
- Dictionaries
- Boolean expressions
- Comparisons
- Strings
- Unsupported operators

For example, this is valid:

```text
(10 + 5) * 2 ** 3
```

while arbitrary Python code is not allowed.

---

## Graphical Interface

The desktop interface is built with:

```text
tkinter
ttk
```

The GUI includes:

- Calculator button grid
- Expression display
- Previous-expression display
- History viewer
- Memory viewer
- Menu bar
- Keyboard support
- Error dialogs
- Application version display

---

## Calculation History

Successful calculations are stored in a history list.

Each history entry contains:

- Timestamp
- Expression
- Result

Example:

```text
2026-09-20 12:00:00 | 2 + 2 = 4
2026-09-20 12:01:00 | 10 / 4 = 2.5
```

History persists between application sessions.

---

## Named Memory Values

Results can be saved into named memory slots.

For example:

```text
tax = 0.08
answer = 42
subtotal = 125.5
```

Saved values can later be inserted back into the calculator.

Memory values are also persisted between application sessions.

---

## Persistent Data Storage

Application data is stored as JSON.

On Windows, the calculator stores its data under the current user's local application-data directory:

```text
%LOCALAPPDATA%\SimpleScientificCalculator\calculator_data.json
```

A typical path looks like:

```text
C:\Users\Username\AppData\Local\SimpleScientificCalculator\calculator_data.json
```

This keeps user-generated data outside the application installation directory and allows packaged versions of the program to safely retain history and memory.

The JSON data contains:

```json
{
    "history": [],
    "memory": {},
    "last_result": null
}
```

---

## Keyboard Controls

The calculator supports normal keyboard input.

### Calculator Keys

| Key | Action |
|---|---|
| `0-9` | Enter numbers |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulus |
| `(` `)` | Parentheses |
| `.` | Decimal point |
| `Enter` | Calculate |
| `Backspace` | Delete last character |
| `Escape` | Clear display |

### Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + H` | Open calculation history |
| `Ctrl + M` | Open saved memory |
| `Ctrl + S` | Save the last result to memory |
| `Ctrl + L` | Clear the display |

---

## Project Structure

```text
Simple_Calculator/
│
├── calculator/
│   ├── __init__.py
│   ├── calculator_engine.py
│   ├── gui.py
│   ├── gui_helpers.py
│   ├── storage.py
│   └── version.py
│
├── tests/
│   ├── test_calculator_engine.py
│   ├── test_gui.py
│   ├── test_gui_helpers.py
│   └── test_storage.py
│
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── release.yml
│
├── .gitignore
├── .pre-commit-config.yaml
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Application Architecture

The project is separated into several modules instead of keeping all functionality in one script.

### `calculator_engine.py`

Contains the calculator's mathematical logic.

Responsibilities include:

- Parsing expressions
- Evaluating AST nodes
- Validating operators
- Formatting numeric results

The calculator engine is independent of the GUI and can be tested directly.

### `storage.py`

Handles application persistence.

Responsibilities include:

- Locating the application-data directory
- Loading JSON data
- Saving JSON data
- History type definitions
- Memory type definitions

### `gui_helpers.py`

Contains non-visual helper logic used by the graphical interface.

Examples include:

- Building formatted history text
- Formatting memory values
- Appending calculator input
- Backspace behavior

Separating this logic from Tkinter makes it easier to test.

### `gui.py`

Contains the Tkinter application.

Responsibilities include:

- Main window
- Menus
- Calculator buttons
- Display
- History window
- Memory window
- Keyboard shortcuts
- User-facing error handling

### `version.py`

Contains the application version:

```python
__version__ = "1.0.0"
```

---

## Requirements

The project currently targets Python 3.12.

Check your Python version:

```bash
python --version
```

Example:

```text
Python 3.12.10
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/BestJustSteve/Simple_Calculator.git
```

Enter the project directory:

```bash
cd Simple_Calculator
```

Install the development dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running the Calculator

Start the application with:

```bash
python main.py
```

---

## Testing

The project uses `pytest`.

Run the complete test suite:

```bash
python -m pytest
```

Run the tests in verbose mode:

```bash
python -m pytest -v
```

The current test suite contains:

```text
83 tests
```

All 83 tests are currently passing.

---

## Test Coverage

Coverage is measured with `pytest-cov`.

Run:

```bash
python -m pytest --cov=calculator --cov-report=term-missing
```

Current coverage:

| Module | Coverage |
|---|---:|
| `calculator_engine.py` | 100% |
| `gui_helpers.py` | 100% |
| `storage.py` | 97% |
| `gui.py` | 40% |
| Overall project | 57% |

The GUI is intentionally tested primarily around application behavior rather than attempting to unit-test every line of Tkinter widget construction.

---

## Code Quality

The project uses several development tools to help maintain code quality.

### Ruff

Ruff is used for linting and formatting.

Check the project:

```bash
python -m ruff check .
```

Automatically fix supported issues:

```bash
python -m ruff check . --fix
```

Format the project:

```bash
python -m ruff format .
```

---

## Static Type Checking

The project uses `mypy` for static type analysis.

Run:

```bash
python -m mypy calculator
```

The application uses type hints throughout the calculator engine, storage layer, GUI helpers, and GUI.

Structured history records use `TypedDict` so that fields such as:

```text
timestamp
expression
result
```

can be checked by mypy.

---

## Pre-Commit Checks

The repository uses `pre-commit` to run development checks before commits.

Install the Git hooks:

```bash
python -m pre_commit install
```

Run all configured hooks manually:

```bash
python -m pre_commit run --all-files
```

The hooks include checks such as:

- Ruff linting
- Ruff formatting
- mypy type checking

---

## Continuous Integration

GitHub Actions is used to automatically validate the project.

The CI workflow can run:

- Dependency installation
- Ruff
- mypy
- pytest
- Test coverage

This helps catch problems before changes are merged or released.

---

## Building the Windows Executable

The application can be packaged into a standalone Windows executable with PyInstaller.

Install PyInstaller:

```bash
python -m pip install pyinstaller
```

Build the executable:

```bash
python -m PyInstaller --onefile --windowed --name SimpleScientificCalculator main.py
```

The resulting executable is created under:

```text
dist/
```

Example:

```text
dist/SimpleScientificCalculator.exe
```

Python does not need to be installed on the computer running the packaged executable.

---

## Versioned Windows Builds

A release build can include the application version in the filename:

```bash
python -m PyInstaller --onefile --windowed --name SimpleScientificCalculator-v1.0.0 main.py
```

This produces:

```text
dist/SimpleScientificCalculator-v1.0.0.exe
```

---

## Releases

The project uses semantic-style version tags such as:

```text
v1.0.0
v1.1.0
v2.0.0
```

The application's internal version is maintained in:

```text
calculator/version.py
```

Example:

```python
__version__ = "1.0.0"
```

Git releases can be tagged with:

```bash
git tag -a v1.0.0 -m "Simple Scientific Calculator v1.0.0"
```

and pushed with:

```bash
git push origin v1.0.0
```

---

## Automated Release Workflow

The repository includes a GitHub Actions release workflow for Windows builds.

When a version tag matching:

```text
v*.*.*
```

is pushed, the workflow can:

1. Check out the repository
2. Install Python
3. Install dependencies
4. Run Ruff
5. Run mypy
6. Run pytest
7. Build the Windows executable
8. Add the version tag to the executable filename
9. Create a GitHub Release
10. Attach the executable to the release

For example:

```bash
git tag -a v1.1.0 -m "Simple Scientific Calculator v1.1.0"
git push origin v1.1.0
```

can produce:

```text
SimpleScientificCalculator-v1.1.0.exe
```

---

## Development Quality Check

Before committing a significant change, the complete local quality check is:

```bash
python -m ruff check .
python -m mypy calculator
python -m pytest --cov=calculator --cov-report=term-missing
```

A successful run should show:

```text
All checks passed!
Success: no issues found
All tests passed
```

---

## Technologies Used

- Python 3.12
- Tkinter
- ttk
- Python AST
- JSON
- pathlib
- pytest
- pytest-cov
- Ruff
- mypy
- pre-commit
- PyInstaller
- Git
- GitHub
- GitHub Actions

---

## Development Goals

This project is also being used as a practical Python software-development learning project.

It demonstrates concepts including:

- Python fundamentals
- Functions
- Classes
- Type hints
- Typed dictionaries
- Exception handling
- File persistence
- JSON serialization
- AST parsing
- GUI development
- Modular application architecture
- Unit testing
- Mocking
- Test coverage
- Static analysis
- Linting
- Automated formatting
- Git version control
- Continuous integration
- Executable packaging
- Automated releases

---

## Future Improvements

Possible future enhancements include:

- Additional memory-management tools
- Improved history searching and filtering
- Exporting calculation history
- User-selectable themes
- Additional keyboard shortcuts
- Scientific calculator functions
- Improved accessibility
- Installer creation
- Automatic version/tag validation
- Additional integration testing
- Release checksums
- Signed Windows builds

---

## Author

**Steve Butler**

GitHub: [BestJustSteve](https://github.com/BestJustSteve)

---

## License

No license has currently been specified for this project.