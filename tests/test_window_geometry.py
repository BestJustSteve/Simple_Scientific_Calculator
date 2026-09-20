from unittest.mock import MagicMock

from calculator.gui import CalculatorApp


def create_app() -> CalculatorApp:
    app = CalculatorApp.__new__(CalculatorApp)

    app.root = MagicMock()

    return app


def test_center_window_sets_geometry():
    app = create_app()

    fake_window = MagicMock()

    fake_window.winfo_screenwidth.return_value = 1920
    fake_window.winfo_screenheight.return_value = 1080

    app.center_window(
        fake_window,
        560,
        790,
    )

    fake_window.update_idletasks.assert_called_once()

    fake_window.geometry.assert_called_once_with("560x790+680+145")


def test_center_window_small_screen_does_not_go_negative():
    app = create_app()

    fake_window = MagicMock()

    fake_window.winfo_screenwidth.return_value = 400
    fake_window.winfo_screenheight.return_value = 300

    app.center_window(
        fake_window,
        560,
        790,
    )

    fake_window.geometry.assert_called_once_with("560x790+0+0")


def test_center_window_square_screen():
    app = create_app()

    fake_window = MagicMock()

    fake_window.winfo_screenwidth.return_value = 1000
    fake_window.winfo_screenheight.return_value = 1000

    app.center_window(
        fake_window,
        500,
        500,
    )

    fake_window.geometry.assert_called_once_with("500x500+250+250")


def test_center_child_window():
    app = create_app()

    app.root.winfo_rootx.return_value = 100
    app.root.winfo_rooty.return_value = 100
    app.root.winfo_width.return_value = 800
    app.root.winfo_height.return_value = 600

    fake_window = MagicMock()

    app.center_child_window(
        fake_window,
        400,
        300,
    )

    app.root.update_idletasks.assert_called_once()
    fake_window.update_idletasks.assert_called_once()

    fake_window.geometry.assert_called_once_with("400x300+300+250")


def test_center_child_window_same_size_as_parent():
    app = create_app()

    app.root.winfo_rootx.return_value = 200
    app.root.winfo_rooty.return_value = 150
    app.root.winfo_width.return_value = 500
    app.root.winfo_height.return_value = 400

    fake_window = MagicMock()

    app.center_child_window(
        fake_window,
        500,
        400,
    )

    fake_window.geometry.assert_called_once_with("500x400+200+150")


def test_center_child_window_larger_than_parent_stays_at_parent_origin():
    app = create_app()

    app.root.winfo_rootx.return_value = 100
    app.root.winfo_rooty.return_value = 75
    app.root.winfo_width.return_value = 300
    app.root.winfo_height.return_value = 200

    fake_window = MagicMock()

    app.center_child_window(
        fake_window,
        500,
        400,
    )

    fake_window.geometry.assert_called_once_with("500x400+100+75")


def test_center_child_window_horizontal_offset():
    app = create_app()

    app.root.winfo_rootx.return_value = 50
    app.root.winfo_rooty.return_value = 50
    app.root.winfo_width.return_value = 1000
    app.root.winfo_height.return_value = 800

    fake_window = MagicMock()

    app.center_child_window(
        fake_window,
        600,
        400,
    )

    fake_window.geometry.assert_called_once_with("600x400+250+250")
