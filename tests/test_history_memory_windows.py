from unittest.mock import MagicMock, patch

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


def test_populate_history_tree():
    app = create_app()

    app.history = [
        {
            "timestamp": "2026-09-20 10:00:00",
            "expression": "2+2",
            "result": 4,
        },
        {
            "timestamp": "2026-09-20 10:01:00",
            "expression": "3*3",
            "result": 9,
        },
    ]

    tree = MagicMock()
    tree.get_children.return_value = []

    app.populate_history_tree(tree)

    assert tree.insert.call_count == 2

    first_call = tree.insert.call_args_list[0]

    assert first_call.kwargs["values"] == (
        "2026-09-20 10:01:00",
        "3*3",
        9,
    )


def test_populate_history_tree_clears_existing_rows():
    app = create_app()

    tree = MagicMock()
    tree.get_children.return_value = [
        "row1",
        "row2",
    ]

    app.populate_history_tree(tree)

    tree.delete.assert_any_call("row1")
    tree.delete.assert_any_call("row2")


def test_use_selected_history_result():
    app = create_app()

    tree = MagicMock()
    tree.selection.return_value = ("0",)
    tree.item.return_value = (
        "2026-09-20 10:00:00",
        "2+2",
        "4",
    )

    window = MagicMock()

    app.previous_var.set("old expression")
    app.just_calculated = True

    app.use_selected_history_result(
        tree,
        window,
    )

    assert app.display_var.get() == "4"
    assert app.previous_var.get() == ""
    assert app.just_calculated is False

    window.destroy.assert_called_once()


def test_use_selected_history_result_without_selection():
    app = create_app()

    tree = MagicMock()
    tree.selection.return_value = ()

    window = MagicMock()

    with patch("calculator.gui.messagebox.showinfo") as mock_info:
        app.use_selected_history_result(
            tree,
            window,
        )

    mock_info.assert_called_once_with(
        "History",
        "Select a history entry first.",
    )

    window.destroy.assert_not_called()


def test_populate_memory_tree():
    app = create_app()

    app.memory = {
        "tax": 0.08,
        "answer": 42,
    }

    tree = MagicMock()
    tree.get_children.return_value = []

    app.populate_memory_tree(tree)

    assert tree.insert.call_count == 2

    first_call = tree.insert.call_args_list[0]
    second_call = tree.insert.call_args_list[1]

    assert first_call.kwargs["iid"] == "answer"
    assert first_call.kwargs["values"] == (
        "answer",
        42,
    )

    assert second_call.kwargs["iid"] == "tax"


def test_populate_memory_tree_clears_existing_rows():
    app = create_app()

    tree = MagicMock()
    tree.get_children.return_value = [
        "old1",
        "old2",
    ]

    app.populate_memory_tree(tree)

    tree.delete.assert_any_call("old1")
    tree.delete.assert_any_call("old2")


def test_use_selected_memory():
    app = create_app()

    app.memory = {
        "answer": 42,
    }

    tree = MagicMock()
    tree.selection.return_value = ("answer",)

    window = MagicMock()

    with patch.object(
        app,
        "use_memory_value",
    ) as mock_use:
        app.use_selected_memory(
            tree,
            window,
        )

    mock_use.assert_called_once_with(
        42,
        window,
    )


def test_use_selected_memory_without_selection():
    app = create_app()

    tree = MagicMock()
    tree.selection.return_value = ()

    window = MagicMock()

    with patch("calculator.gui.messagebox.showinfo") as mock_info:
        app.use_selected_memory(
            tree,
            window,
        )

    mock_info.assert_called_once_with(
        "Memory",
        "Select a memory value first.",
    )


def test_use_selected_memory_missing_value():
    app = create_app()

    tree = MagicMock()
    tree.selection.return_value = ("missing",)

    window = MagicMock()

    with patch("calculator.gui.messagebox.showerror") as mock_error:
        app.use_selected_memory(
            tree,
            window,
        )

    mock_error.assert_called_once_with(
        "Memory",
        "That memory value is no longer available.",
    )


def test_delete_selected_memory():
    app = create_app()

    app.memory = {
        "answer": 42,
        "tax": 0.08,
    }

    tree = MagicMock()
    tree.selection.return_value = ("answer",)

    with (
        patch.object(
            app,
            "save",
        ) as mock_save,
        patch.object(
            app,
            "populate_memory_tree",
        ) as mock_populate,
    ):
        app.delete_selected_memory(tree)

    assert "answer" not in app.memory
    assert "tax" in app.memory

    mock_save.assert_called_once()
    mock_populate.assert_called_once_with(tree)


def test_delete_selected_memory_without_selection():
    app = create_app()

    tree = MagicMock()
    tree.selection.return_value = ()

    with (
        patch("calculator.gui.messagebox.showinfo") as mock_info,
        patch.object(
            app,
            "save",
        ) as mock_save,
    ):
        app.delete_selected_memory(tree)

    mock_info.assert_called_once_with(
        "Memory",
        "Select a memory value first.",
    )

    mock_save.assert_not_called()


def test_delete_selected_memory_missing_value():
    app = create_app()

    app.memory = {
        "answer": 42,
    }

    tree = MagicMock()
    tree.selection.return_value = ("missing",)

    with patch.object(
        app,
        "save",
    ) as mock_save:
        app.delete_selected_memory(tree)

    assert app.memory == {"answer": 42}

    mock_save.assert_not_called()


def test_history_results_are_displayed_newest_first():
    app = create_app()

    app.history = [
        {
            "timestamp": "older",
            "expression": "1+1",
            "result": 2,
        },
        {
            "timestamp": "newer",
            "expression": "2+2",
            "result": 4,
        },
    ]

    tree = MagicMock()
    tree.get_children.return_value = []

    app.populate_history_tree(tree)

    first_values = tree.insert.call_args_list[0].kwargs["values"]

    assert first_values[0] == "newer"
    assert first_values[1] == "2+2"
    assert first_values[2] == 4


def test_memory_values_are_sorted_by_name():
    app = create_app()

    app.memory = {
        "zebra": 3,
        "alpha": 1,
        "middle": 2,
    }

    tree = MagicMock()
    tree.get_children.return_value = []

    app.populate_memory_tree(tree)

    names = [call.kwargs["iid"] for call in tree.insert.call_args_list]

    assert names == [
        "alpha",
        "middle",
        "zebra",
    ]
